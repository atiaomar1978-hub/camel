#!/usr/bin/env bash
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

# Source this file to configure Java for Apache Camel builds on macOS (Homebrew):
#   source scripts/dev-java-env.sh
#
# Prefers OpenJDK 21 (Camel 4.x requires Java 17+). Falls back to openjdk or openjdk@24.

set_java_home_from_brew() {
  local candidate
  for candidate in \
    "/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home" \
    "/usr/local/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home" \
    "/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home" \
    "/opt/homebrew/opt/openjdk@24/libexec/openjdk.jdk/Contents/Home"; do
    if [[ -x "${candidate}/bin/java" ]]; then
      export JAVA_HOME="${candidate}"
      export PATH="${JAVA_HOME}/bin:${PATH}"
      return 0
    fi
  done
  return 1
}

if ! set_java_home_from_brew; then
  echo "No Homebrew OpenJDK found. Install with: brew install openjdk@21" >&2
  return 1 2>/dev/null || exit 1
fi

echo "JAVA_HOME=${JAVA_HOME}"
java -version
