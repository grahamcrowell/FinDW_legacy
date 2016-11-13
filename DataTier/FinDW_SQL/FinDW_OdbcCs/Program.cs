using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using System.Data.Odbc;

namespace FinDW_OdbcCs
{
    class Program
    {
        public static void show(DataTable dataTable)
        {
            foreach (DataColumn column in dataTable.Columns)
            {
                Console.WriteLine(column.ColumnName);
                Console.WriteLine(column.DataType);
            }
            foreach (DataRow row in dataTable.Rows)
            {
                Console.WriteLine(row);
            }
        }
        public static void test_odbc()
        {
            OdbcConnectionStringBuilder cxStr = new OdbcConnectionStringBuilder();
            cxStr.Dsn = "MsSqlOdbcX86_FinDW";
            cxStr.Driver = "ODBC Driver 13 for SQL Server";
            Console.WriteLine(cxStr.ConnectionString);
            OdbcConnection cx = new OdbcConnection(cxStr.ConnectionString);
            cx.Open();
            DataTable metaData = cx.GetSchema();
            Console.WriteLine(metaData);
            show(metaData);
        }
        static void Main(string[] args)
        {
            test_odbc();
            Console.ReadKey();
        }
    }
}
