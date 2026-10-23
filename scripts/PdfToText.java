import java.io.File;

import org.apache.pdfbox.Loader;
import org.apache.pdfbox.text.PDFTextStripper;

/**
 * Converts a PDF to text the same way Portfolio Performance does
 * (PDFBox3Adapter and PDFInputFile.sanitize).
 */
public class PdfToText
{
    public static void main(String[] args) throws Exception
    {
        try (var document = Loader.loadPDF(new File(args[0])))
        {
            var stripper = new PDFTextStripper();
            stripper.setSortByPosition(true);
            System.out.print(stripper.getText(document).replaceAll("\\h", " ").replace("\r", ""));
        }
    }
}
