

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Date;

import org.apache.commons.lang3.StringUtils;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;


public class SvnLogToExcel3 {

    private static final String Author = "Author: ";
    
    private static final String Version = "Revision: ";
    
    private static final String Message = "Message:";
    
    private static final String Modified = "Modified :";
    
    private static final String Added = "Added :";
    
    private static final String Deleted = "Deleted :";
    
    private static final String MsgEnd = "----";
    
    public static void main(String[] args) {
        
        String svnFile = "F:/daimagengxin.txt";
        
        // author description requirement
        Map<Integer, String[]> version2ADR = new HashMap<>();
        // string = Action +  DocumentName, care the " :"
        Map<Integer, List<String>> version2Docu = new TreeMap<>(new Comparator<Integer>() {
            public int compare(Integer o1, Integer o2) {
                return o1 == o2 ? 0 : o1 > o2 ? -1 : 1;
            }
        });
        
        BufferedReader reader = null;
        String temp = null;
        Integer vers = null;
        String auth = null;
        String desc = null;
//        String requ = null;
        String docu = null;
        
        int lenVersion = Version.length();
        int lenAuthor = Author.length();
        boolean isMsg = false;
        String[] strArr = null;
        
        String regEx2 = "\\d+\\.\\d+";
        Pattern p2 = Pattern.compile(regEx2);
        Matcher m = null;
        List<String> docuList = null;
        
        String regEx3 = "mantis\\s*[0-9]*";
        Pattern p3 = Pattern.compile(regEx3);
        
        try {
            reader = new BufferedReader(new InputStreamReader(new FileInputStream(svnFile), "gbk"));
            
            while((temp = reader.readLine()) != null)
            {
                if(!isMsg && temp.startsWith(Version))
                {
                    if(docuList != null && !docuList.isEmpty())
                    {
                        version2Docu.put(vers, docuList);
                    }
                    docuList = new ArrayList<>();
                    vers = Integer.valueOf(temp.substring(lenVersion));
                    continue;
                }
                
                if(!isMsg && temp.startsWith(Author))
                {
                    auth = temp.substring(lenAuthor);
                    continue;
                }
                
                if(!isMsg && temp.startsWith(Message))
                {
                    isMsg = true;
                    continue;
                }
                
                if(isMsg)
                {
                    if(isMsg && temp.startsWith(MsgEnd) && temp.endsWith(MsgEnd))
                    {
                        strArr = new String[3];
                        strArr[0] = auth;
                        strArr[1] = desc;
                        if ((m = p2.matcher(desc)).find()) {
                            strArr[2] = m.group();
                        } else if ((m = p3.matcher(desc)).find()) {
                            strArr[2] = StringUtils.deleteWhitespace(m.group());
                        } else {
                            strArr[2] = StringUtils.EMPTY;
                        }
                        version2ADR.put(vers, strArr);
                        
                        desc = null;
                        isMsg = false;
                        continue;
                    }
                    
                    if(desc == null || desc.length() == 0)
                    {
                        desc = temp;
                    }
                    else
                    {
                        desc += "\n";
                        desc += temp;
                    }
                    continue;
                }
                
                if(!isMsg && temp.startsWith(Deleted))
                {
                    docu = Deleted + temp.substring(temp.lastIndexOf('/') + 1);
                    docuList.add(docu);
                    continue;
                }
                
                if(!isMsg && temp.startsWith(Added))
                {
                    docu = Added + temp.substring(temp.lastIndexOf('/') + 1);
                    docuList.add(docu);
                    continue;
                }
                
                if(!isMsg && temp.startsWith(Modified))
                {
                    docu = Modified + temp.substring(temp.lastIndexOf('/') + 1);
                    docuList.add(docu);
                    continue;
                }
                
            }
            
            // ...
            if(docuList != null && !docuList.isEmpty())
            {
                version2Docu.put(vers, docuList);
            }
            
//            for(Map.Entry<Integer, String[]> entry : version2ADR.entrySet())
//            {
//                System.out.println(entry.getKey() + "\n    " + StringUtils.join(entry.getValue(), ','));
//            }
//            
//            for(Map.Entry<Integer, List<String>> entry : version2Docu.entrySet())
//            {
//                System.out.println(entry.getKey() + "\n    " + StringUtils.join(entry.getValue(), ','));
//            }
            
            
        } catch (UnsupportedEncodingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } finally {
            try {
                reader.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        
        String out1 = "F:/代码更新自动创建_格式2_" + new SimpleDateFormat("yyyy-MM-dd").format(new Date()) + "_" + new Date().getTime() / 1000 % 10000 + ".xlsx";
        
        XSSFWorkbook workbook = new XSSFWorkbook();
        // delete is NO.1
        XSSFSheet sh3 = workbook.createSheet("删除");
        XSSFSheet sh1 = workbook.createSheet("全部");
        XSSFSheet sh2 = workbook.createSheet("最新(包含删除)");
        
        sh1.setColumnWidth(0, 3000);
        sh1.setColumnWidth(1, 12000);
        sh1.setColumnWidth(2, 2000);
        sh1.setColumnWidth(3, 4000);
        sh1.setColumnWidth(4, 3000);
        sh1.setColumnWidth(5, 20000);
        
        XSSFRow row = null;
        XSSFCell ce0 = null;
        XSSFCell ce1 = null;
        XSSFCell ce2 = null;
        XSSFCell ce3 = null;
        XSSFCell ce4 = null;
        XSSFCell ce5 = null;
        
        int i = 0;
        row = sh1.createRow(i);
        ce0 = row.createCell(0);
        ce1 = row.createCell(1);
        ce2 = row.createCell(2);
        ce3 = row.createCell(3);
        ce4 = row.createCell(4);
        ce5 = row.createCell(5);
        ce0.setCellValue("操作");
        ce1.setCellValue("文件名");
        ce2.setCellValue("版本");
        ce3.setCellValue("需求点");
        ce4.setCellValue("上传者");
        ce5.setCellValue("描述");
        row.createCell(6).setCellValue("检查者");
        
        String[] strArr2 = null;
        
        Map<String, Data> docu2HighestV = new HashMap<>();
        Data data = null;
        Data2 data2 = null;
        List<Data2> deleteList = new ArrayList<>();
        
        for(Map.Entry<Integer, List<String>> entry : version2Docu.entrySet())
        {
            docuList = entry.getValue();
            strArr = version2ADR.get(entry.getKey());
            
            for(String str : docuList)
            {
                i++;
                row = sh1.createRow(i);
                ce0 = row.createCell(0);
                ce1 = row.createCell(1);
                ce2 = row.createCell(2);
                ce3 = row.createCell(3);
                ce4 = row.createCell(4);
                ce5 = row.createCell(5);
                strArr2 = str.split(" :");
                ce0.setCellValue(strArr2[0]);   // action
                ce1.setCellValue(strArr2[1]);   // document name
                ce2.setCellValue(entry.getKey());   // reversion
                ce3.setCellValue(strArr[2]);    // requirement number
                ce4.setCellValue(strArr[0]);    // author
                ce5.setCellValue(strArr[1]);    // description
                
                SvnLogToExcel3 t = new SvnLogToExcel3();
                
                if(!docu2HighestV.containsKey(strArr2[1]))
                {
//                    data = t.new Data();
                    data = new Data();
                    data.action = strArr2[0];
                    data.version = entry.getKey();
                    data.author = strArr[0];
                    docu2HighestV.put(strArr2[1], data);
                }
                
                if(Deleted.startsWith(strArr2[0]))
                {
                    data2 = t.new Data2();
                    data2.docuName = strArr2[1];
                    data2.version = entry.getKey();
                    deleteList.add(data2);
                }
            }
        }
        
        
        i = 0;
        row = sh2.createRow(i);
        ce0 = row.createCell(0);
        ce1 = row.createCell(1);
        ce2 = row.createCell(2);
        ce3 = row.createCell(3);
        sh2.setColumnWidth(0, 3000);
        sh2.setColumnWidth(1, 12000);
        sh2.setColumnWidth(3, 3000);
        ce0.setCellValue("操作");
        ce1.setCellValue("文件名");
        ce2.setCellValue("最高版本");
        ce3.setCellValue("最后更新者");
        
        for(Map.Entry<String, Data> entry : docu2HighestV.entrySet())
        {
            i++;
            row = sh2.createRow(i);
            ce0 = row.createCell(0);
            ce1 = row.createCell(1);
            ce2 = row.createCell(2);
            ce3 = row.createCell(3);
            ce0.setCellValue(entry.getValue().action);
            ce1.setCellValue(entry.getKey());
            ce2.setCellValue(entry.getValue().version);
            ce3.setCellValue(entry.getValue().author);
        }
        
        
        i = 0;
        row = sh3.createRow(i);
        ce0 = row.createCell(0);
        ce1 = row.createCell(1);
        ce2 = row.createCell(2);
        sh3.setColumnWidth(0, 3000);
        sh3.setColumnWidth(1, 12000);
        ce0.setCellValue("操作");
        ce1.setCellValue("文件名");
        ce2.setCellValue("版本");
        
        for(Data2 d : deleteList)
        {
            i++;
            row = sh3.createRow(i);
            ce0 = row.createCell(0);
            ce1 = row.createCell(1);
            ce2 = row.createCell(2);
            ce3 = row.createCell(3);
            
            ce0.setCellValue("Delete");
            ce1.setCellValue(d.docuName);
            ce2.setCellValue(d.version);
        }
        
        
        
        FileOutputStream out;
        try {
            out = new FileOutputStream(out1);
            workbook.write(out);
            workbook.close();
            out.close();
            System.out.print("done");
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
    }
    
    // 最高版本
    private static final class Data {
        public Integer version;
        public String action;
        public String author;
    }
    
    // delete
    private final class Data2
    {
        public Integer version;
        public String docuName;
    }
}
