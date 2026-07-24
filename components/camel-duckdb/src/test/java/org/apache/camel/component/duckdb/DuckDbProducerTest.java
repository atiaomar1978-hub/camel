/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.camel.component.duckdb;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import org.apache.camel.test.junit6.CamelTestSupport;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import static org.assertj.core.api.Assertions.assertThat;

class DuckDbProducerTest extends CamelTestSupport {

    private static String jdbcEndpoint(Path dbFile) {
        String jdbcUrl = "jdbc:duckdb:" + dbFile.toAbsolutePath();
        return "duckdb::memory:?jdbcUrl=" + URLEncoder.encode(jdbcUrl, StandardCharsets.UTF_8);
    }

    @Test
    void insertAndQueryRows(@TempDir Path tempDir) throws Exception {
        String uri = jdbcEndpoint(tempDir.resolve("test.db"));
        template.sendBody(uri + "&operation=execute", "CREATE TABLE events (id INTEGER, name VARCHAR)");
        template.sendBody(uri + "&operation=insert&table=events", List.of(Map.of("id", 1, "name", "ada")));

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> rows = template.requestBody(uri + "&operation=query", "SELECT name FROM events", List.class);
        assertThat(rows).hasSize(1);
        assertThat(rows.get(0).get("name")).isEqualTo("ada");
    }

    @Test
    void copyFromCsvFile(@TempDir Path tempDir) throws Exception {
        Path dbFile = tempDir.resolve("test.db");
        String uri = jdbcEndpoint(dbFile);
        template.sendBody(uri + "&operation=execute", "CREATE TABLE events (id INTEGER, name VARCHAR)");

        Path csv = tempDir.resolve("data.csv");
        Files.writeString(csv, "id,name\n2,bob\n");

        template.sendBody(uri + "&operation=copy&table=events&format=csv", csv.toFile());

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> rows = template.requestBody(uri + "&operation=query", "SELECT name FROM events WHERE id = 2",
                List.class);
        assertThat(rows).extracting(row -> row.get("name")).containsExactly("bob");
    }
}
