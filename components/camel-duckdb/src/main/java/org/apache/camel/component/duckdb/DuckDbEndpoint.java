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

import java.sql.Connection;
import java.sql.DriverManager;

import javax.sql.DataSource;

import org.apache.camel.Category;
import org.apache.camel.Consumer;
import org.apache.camel.Processor;
import org.apache.camel.Producer;
import org.apache.camel.spi.Metadata;
import org.apache.camel.spi.UriEndpoint;
import org.apache.camel.spi.UriParam;
import org.apache.camel.spi.UriPath;
import org.apache.camel.support.DefaultEndpoint;
import org.apache.camel.util.ObjectHelper;

/**
 * Interact with <a href="https://duckdb.org/">DuckDB</a>, the in-process analytical SQL database, for embedded
 * analytics workloads.
 */
@UriEndpoint(firstVersion = "4.22.0", scheme = "duckdb", title = "DuckDB",
             syntax = "duckdb:databasePath", category = { Category.DATABASE, Category.BIGDATA },
             producerOnly = true, headersClass = DuckDbConstants.class)
public class DuckDbEndpoint extends DefaultEndpoint {

    private DataSource dataSource;
    private Connection connection;
    private Connection injectedConnection;
    private boolean connectionOwned;

    @UriPath(description = "Database path (:memory: or a file path). An optional /table segment sets the default table.")
    private String databasePath = ":memory:";
    @UriParam(description = "Target table for insert and copy operations. Can also be set in the path as databasePath/table"
                            + " or overridden with the CamelDuckDbTable header.")
    private String table;
    @UriParam(description = "Full JDBC URL override. When set, databasePath is not used to build the URL.")
    private String jdbcUrl;
    @UriParam(defaultValue = "EXECUTE", description = "The operation to perform: execute, query, insert, copy or ping.")
    private DuckDbOperation operation = DuckDbOperation.EXECUTE;
    @UriParam(description = "Static SQL for query when the message body is empty.")
    private String query;
    @UriParam(defaultValue = "0",
              description = "Batch size for insert when the body is a List. 0 inserts all rows in one JDBC batch.")
    private int batchSize;
    @UriParam(defaultValue = "auto",
              description = "File format for copy: csv, parquet, json or auto (inferred from the file extension).")
    private String format = "auto";
    @UriParam(defaultValue = "false", description = "Open the embedded database file in read-only mode when supported.")
    private boolean readOnly;
    @UriParam(defaultValue = "LIST_MAP",
              description = "How query results are returned: LIST_MAP (List of Map) or JSON array string.")
    private DuckDbResultFormat resultFormat = DuckDbResultFormat.LIST_MAP;

    public DuckDbEndpoint() {
    }

    public DuckDbEndpoint(String uri, DuckDbComponent component) {
        super(uri, component);
    }

    @Override
    public Producer createProducer() throws Exception {
        return new DuckDbProducer(this);
    }

    @Override
    public Consumer createConsumer(Processor processor) throws Exception {
        throw new UnsupportedOperationException("You cannot receive messages from this endpoint");
    }

    Connection getConnectionForProducer() throws Exception {
        if (injectedConnection != null) {
            return injectedConnection;
        }
        if (connection != null && !connection.isClosed()) {
            return connection;
        }
        if (dataSource != null) {
            return dataSource.getConnection();
        }
        throw new IllegalStateException("DuckDB connection is not available");
    }

    @Override
    protected void doStart() throws Exception {
        super.doStart();
        if (injectedConnection != null || dataSource != null) {
            return;
        }
        String url = DuckDbJdbcSupport.resolveJdbcUrl(jdbcUrl, databasePath);
        connection = DriverManager.getConnection(url);
        connectionOwned = true;
    }

    @Override
    protected void doStop() throws Exception {
        if (connectionOwned && connection != null) {
            connection.close();
            connection = null;
            connectionOwned = false;
        }
        super.doStop();
    }

    void setConnectionForTesting(Connection connection) {
        this.injectedConnection = connection;
    }

    public DataSource getDataSource() {
        return dataSource;
    }

    public void setDataSource(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public String getDatabasePath() {
        return databasePath;
    }

    public void setDatabasePath(String databasePath) {
        this.databasePath = databasePath;
    }

    public String getTable() {
        return table;
    }

    public void setTable(String table) {
        this.table = table;
    }

    public String getJdbcUrl() {
        return jdbcUrl;
    }

    public void setJdbcUrl(String jdbcUrl) {
        this.jdbcUrl = jdbcUrl;
    }

    public DuckDbOperation getOperation() {
        return operation;
    }

    public void setOperation(DuckDbOperation operation) {
        this.operation = operation;
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public int getBatchSize() {
        return batchSize;
    }

    public void setBatchSize(int batchSize) {
        this.batchSize = batchSize;
    }

    public String getFormat() {
        return format;
    }

    public void setFormat(String format) {
        this.format = format;
    }

    public boolean isReadOnly() {
        return readOnly;
    }

    public void setReadOnly(boolean readOnly) {
        this.readOnly = readOnly;
    }

    public DuckDbResultFormat getResultFormat() {
        return resultFormat;
    }

    public void setResultFormat(DuckDbResultFormat resultFormat) {
        this.resultFormat = resultFormat;
    }

    String resolvedJdbcUrl() {
        return DuckDbJdbcSupport.resolveJdbcUrl(jdbcUrl, databasePath);
    }

    boolean usesExternalConnection() {
        return injectedConnection != null || dataSource != null;
    }
}
