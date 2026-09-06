#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Helpers for parsing Maven reactor timing lines from incremental-test.log.

parse_reactor_duration_seconds() {
  local line="$1"
  if [[ "$line" =~ \[[[:space:]]*([0-9]+(\.[0-9]+)?)[[:space:]]*s\][[:space:]]*$ ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi
  echo ""
}

parse_reactor_status() {
  local line="$1"
  if [[ "$line" =~ [[:space:]](SUCCESS|FAILURE|SKIPPED)[[:space:]]*\[ ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi
  if [[ "$line" =~ [[:space:]](SUCCESS|FAILURE|SKIPPED)[[:space:]]*$ ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi
  echo ""
}

parse_reactor_module_name() {
  local line="$1"
  local name="${line#\[INFO\] }"
  name=$(echo "$name" | sed 's/ \..*$//')
  name=$(echo "$name" | sed 's/  *\[.*\]$//')
  name=$(echo "$name" | sed 's/ SUCCESS$//; s/ FAILURE$//; s/ SKIPPED$//')
  name=$(echo "$name" | sed 's/  *$//')
  echo "$name"
}

format_elapsed_seconds() {
  local raw="$1"
  if [[ -z "$raw" ]]; then
    echo "n/a"
    return 0
  fi

  awk -v seconds="$raw" '
    BEGIN {
      if (seconds < 60) {
        printf "%.1fs", seconds
      } else {
        mins = int(seconds / 60)
        secs = seconds - (mins * 60)
        if (mins < 60) {
          printf "%dm %.0fs", mins, secs
        } else {
          hours = int(mins / 60)
          mins = mins - (hours * 60)
          printf "%dh %dm", hours, mins
        }
      }
    }'
}

parse_reactor_log_to_tsv() {
  local log_file="$1"
  local parsed=""
  local line module duration status

  while IFS= read -r line; do
    module=$(parse_reactor_module_name "$line")
    duration=$(parse_reactor_duration_seconds "$line")
    status=$(parse_reactor_status "$line")
    if [[ -n "$module" ]]; then
      parsed+="${module}"$'\t'"${duration}"$'\t'"${status}"$'\n'
    fi
  done < <(grep '^\[INFO\] Camel ::' "$log_file" || true)

  if [[ -z "$parsed" ]]; then
    return 0
  fi

  echo "$parsed" | awk -F '\t' '
    {
      key = $1
      if (key == "") {
        next
      }
      duration = ($2 == "" ? -1 : $2)
      status = $3
      if (!(key in seen) || duration > stored[key]) {
        seen[key] = 1
        stored[key] = duration
        statuses[key] = status
      }
    }
    END {
      for (key in seen) {
        duration = stored[key]
        if (duration < 0) {
          duration = ""
        }
        printf "%s\t%s\t%s\n", key, duration, statuses[key]
      }
    }' | sort
}

sum_elapsed_seconds_from_tsv() {
  local tsv="$1"
  if [[ -z "$tsv" ]]; then
    echo "0"
    return 0
  fi
  echo "$tsv" | awk -F '\t' '
    $2 != "" && $2 ~ /^[0-9]+(\.[0-9]+)?$/ { total += $2 }
    END { printf "%.3f", total + 0 }'
}

render_top_slowest_modules() {
  local tsv="$1"
  local limit="${2:-5}"
  echo "$tsv" | awk -F '\t' '
    $2 != "" && $2 ~ /^[0-9]+(\.[0-9]+)?$/ {
      printf "%s\t%s\n", $2, $1
    }' | sort -t $'\t' -k1,1nr | head -n "$limit" | while IFS=$'\t' read -r seconds module; do
    local formatted
    formatted=$(format_elapsed_seconds "$seconds")
    echo "- \`${module}\` (${formatted})"
  done
}

append_reactor_timing_report() {
  local log_file="$1"
  local comment_file="$2"
  local reactor_label="$3"
  local step_summary_file="${4:-}"

  if [[ ! -f "$log_file" ]]; then
    return 0
  fi

  local tsv
  tsv=$(parse_reactor_log_to_tsv "$log_file")
  if [[ -z "$tsv" ]]; then
    return 0
  fi

  local count total_seconds total_formatted
  count=$(echo "$tsv" | grep -c . || true)
  total_seconds=$(sum_elapsed_seconds_from_tsv "$tsv")
  total_formatted=$(format_elapsed_seconds "$total_seconds")

  {
    echo ""
    echo "<details><summary>${reactor_label} (${count} modules, ${total_formatted} total)</summary>"
    echo ""
    echo "**Total reactor time:** ${total_formatted}"
    echo ""
    echo "| Module | Duration | Status |"
    echo "| --- | --- | --- |"
  } >> "$comment_file"

  echo "$tsv" | awk -F '\t' '
    $2 != "" && $2 ~ /^[0-9]+(\.[0-9]+)?$/ {
      printf "%s\t%s\t%s\n", $2, $1, $3
    }
    $2 == "" {
      printf "-1\t%s\t%s\n", $1, $3
    }' | sort -t $'\t' -k1,1nr | while IFS=$'\t' read -r sort_key module status; do
    local duration_display="n/a"
    if [[ "$sort_key" != "-1" ]]; then
      duration_display=$(format_elapsed_seconds "$sort_key")
    fi
    echo "| ${module} | ${duration_display} | ${status:-} |" >> "$comment_file"
  done

  local slowest
  slowest=$(render_top_slowest_modules "$tsv" 5)
  if [[ -n "$slowest" ]]; then
    {
      echo ""
      echo "**Top 5 slowest modules:**"
      echo "$slowest"
    } >> "$comment_file"
  fi

  {
    echo ""
    echo "</details>"
  } >> "$comment_file"

  if [[ -n "$step_summary_file" ]]; then
    {
      echo ""
      echo "<details><summary><b>${reactor_label} (${count} modules, ${total_formatted} total)</b></summary>"
      echo ""
      echo "**Total reactor time:** ${total_formatted}"
      echo ""
      echo "| Module | Duration | Status |"
      echo "| --- | --- | --- |"
    } >> "$step_summary_file"

    echo "$tsv" | awk -F '\t' '
      $2 != "" && $2 ~ /^[0-9]+(\.[0-9]+)?$/ {
        printf "%s\t%s\t%s\n", $2, $1, $3
      }
      $2 == "" {
        printf "-1\t%s\t%s\n", $1, $3
      }' | sort -t $'\t' -k1,1nr | while IFS=$'\t' read -r sort_key module status; do
      local duration_display="n/a"
      if [[ "$sort_key" != "-1" ]]; then
        duration_display=$(format_elapsed_seconds "$sort_key")
      fi
      echo "| ${module} | ${duration_display} | ${status:-} |" >> "$step_summary_file"
    done

    if [[ -n "$slowest" ]]; then
      {
        echo ""
        echo "**Top 5 slowest modules:**"
        echo "$slowest"
      } >> "$step_summary_file"
    fi

    {
      echo ""
      echo "</details>"
    } >> "$step_summary_file"
  fi
}
