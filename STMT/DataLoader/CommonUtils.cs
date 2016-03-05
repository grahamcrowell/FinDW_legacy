using Microsoft.SqlServer.Management.Smo;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataLoader
{
	public static class CommonUtils
	{
		#region User Interface Methods
		public static void user_exit()
		{
			Console.WriteLine("\r\n\r\nexecution complete\r\npress enter key to exit");
			while (Console.ReadKey().Key != ConsoleKey.Escape && Console.ReadKey().Key != ConsoleKey.Enter) { }
		}
		public static string cwd()
		{
			string path = Directory.GetCurrentDirectory();
			Console.WriteLine("The current directory is {0}", path);
			return path;
		}
		public static string cwd(string new_dir)
		{
			if (!Directory.Exists(new_dir))
			{
				Directory.CreateDirectory(new_dir);
			}
			Directory.SetCurrentDirectory(new_dir);
			return cwd();
		}
		#endregion
		#region SMO methods
		public static Database get_database(string server_name, string database_name)
		{
			Server srv = new Server(server_name);
			Database db;
			//Console.WriteLine("Press 'Y' to connect to database: {0}.{2} ({1})", srv.ToString(), srv.Information.Version, database_name);
			ConsoleKeyInfo key;
			//key = Console.ReadKey();
			//if (key.KeyChar == 'y')
			if (1 == 1)
			{
				if (srv.Databases.Contains(database_name))
				{
					Console.WriteLine("\r\nconnecting to: {0}.{2} ({1})", srv.ToString(), srv.Information.Version, database_name);
					// Reference the database.  
					db = srv.Databases[database_name];
				}
				else
				{
					Console.WriteLine("Press 'Y' to create database_name: {0}.{2} ({1})", srv.ToString(), srv.Information.Version, database_name);
					key = Console.ReadKey();
					if (key.KeyChar == 'y')
					{
						db = new Database(srv, database_name);
						db.Create();
					}
					else
					{
						Console.WriteLine(string.Format("skipping database: {0}", database_name));
						return null;
					}
				}
			}
			else
			{
				Console.WriteLine(string.Format("skipping database: {0}", database_name));
				return null;
			}
			return db;
		}
		public static string get_connection_string(string server_name, string database_name)
		{
			string fmt = "Data Source={0};Initial Catalog={1};Integrated Security=true;";
			return string.Format(fmt, server_name, database_name);
		}
		public static SqlConnection get_sql_connection(string server_name, string database_name)
		{
			return new SqlConnection(get_connection_string(server_name, database_name));
		}
		#endregion
		#region Custom fusion methods
		public static int get_shot_no(string path)
		{
			int x;
			string y = Path.GetDirectoryName(path);
			//Console.WriteLine(y);
			string z = Path.GetDirectoryName(y);
			//Console.WriteLine(z);
			x = Int32.Parse(Path.GetFileName(z));
			//Console.WriteLine(x);
			return x;
		}
		public static string get_x_type(string path)
		{
			string y = Path.GetDirectoryName(path);
			//Console.WriteLine(y);
			//string z = Path.GetDirectoryName(y);
			//Console.WriteLine(z);
			//x = Int32.Parse(Path.GetFileName(y));
			//Console.WriteLine(x);
			return Path.GetFileName(y);
		}
		#endregion
	}
}