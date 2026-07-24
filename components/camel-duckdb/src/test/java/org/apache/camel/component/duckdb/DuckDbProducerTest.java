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

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.component.mock.MockEndpoint;
import org.apache.camel.test.junit6.CamelTestSupport;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import static org.assertj.core.api.Assertions.assertThat;

class DuckDbProducerTest extends CamelTestSupport {

    @TempDir
    Path tempDir;

    private String endpointBase;

    @BeforeEach
    void createSchema() throws Exception {
        Path dbFile = tempDir.resolve("test.db");
        String jdbcUrl = "jdbc:duckdb:" + dbFile.toAbsolutePath();
        endpointBase = "duckdb:?jdbcUrl=" + URLEncoder.encode(jdbcUrl, StandardCharsets.UTF_8);
        template.sendBody(endpointBase + "&operation=execute", "CREATE TABLE events (id INTEGER, name VARCHAR)");
        template.sendBody(endpointBase + "&operation=execute", "DELETE FROM events");
    }

    @Override
    protected RouteBuilder createRouteBuilder() {
        return new RouteBuilder() {
            @Override
            public void configure() {
                from("direct:insert")
                        .toD("${header.DuckDbTestUri}?operation=insert&table=events")
                        .to("mock:inserted");
                from("direct:query")
                        .toD("${header.DuckDbTestUri}?operation=query")
                        .to("mock:queried");
                from("direct:copy")
                        .toD("${header.DuckDbTestUri}?operation=copy&table=events&format=csv")
                        .to("mock:copied");
            }
        };
    }

    @Test
    void insertAndQueryRows() throws Exception {
        MockEndpoint inserted = getMockEndpoint("mock:inserted");
        inserted.expectedMessageCount(1);

        template.send("direct:insert", exchange -> {
            exchange.getIn().setHeader("DuckDbTestUri", endpointBase);
            exchange.getIn().setBody(List.of(Map.of("id", 1, "name", "ada")));
        });

        MockEndpoint.assertIsSatisfied(context);

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> rows = template.request("direct:query", exchange -> {
            exchange.getIn().setHeader("DuckDbTestUri", endpointBase);
            exchange.getIn().setBody("SELECT name FROM events");
        }).getMessage().getBody(List.class);
        assertThat(rows).hasSize(1);
        assertThat(rows.get(0).get("name")).isEqualTo("ada");
    }

    @Test
    void copyFromCsvFile() throws Exception {
        Path csv = tempDir.resolve("data.csv");
        Files.writeString(csv, "id,name\n2,bob\n");

        MockEndpoint copied = getMockEndpoint("mock:copied");
        copied.expectedMessageCount(1);

        template.send("direct:copy", exchange -> {
            exchange.getIn().setHeader("DuckDbTestUri", endpointBase);
            exchange.getIn().setBody(csv.toFile());
        });

        MockEndpoint.assertIsSatisfied(context);

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> rows = template.request("direct:query", exchange -> {
            exchange.getIn().setHeader("DuckDbTestUri", endpointBase);
            exchange.getIn().setBody("SELECT name FROM events WHERE id = 2");
        }).getMessage().getBody(List.class);
        assertThat(rows).extracting(row -> row.get("name")).containsExactly("bob");
    }
}
