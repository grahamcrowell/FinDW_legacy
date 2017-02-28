using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Schema;
using System.Xml.XPath;

namespace BimlCsGenerator
{
    class Program
    {
        public static void test_readSchema()
        {
            XmlReaderSettings booksSettings = new XmlReaderSettings();

            var xmlSchema = booksSettings.Schemas.Add("http://schemas.varigence.com/biml.xsd", "biml.xsd");
            booksSettings.ValidationType = ValidationType.Schema;
            booksSettings.ValidationEventHandler += new ValidationEventHandler(bimlSettingsValidationEventHandler);

            XmlReader books = XmlReader.Create("findw.biml", booksSettings);
            while (books.Read()) { }

        }
        public static void bimlSettingsValidationEventHandler(object sender, ValidationEventArgs e)
        {
            if (e.Severity == XmlSeverityType.Warning)
            {
                Console.Write("WARNING: ");
                Console.WriteLine(e.Message);
            }
            else if (e.Severity == XmlSeverityType.Error)
            {
                Console.Write("ERROR: ");
                Console.WriteLine(e.Message);
            }
        }
        static void Main(string[] args)
        {
            test_readSchema();
            Console.ReadKey();
        }
    }
}
