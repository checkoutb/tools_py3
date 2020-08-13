

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Date;

import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class SvnLogToExcel1 {

    public static void main(String[] args) throws IOException {
        
        Map<String, Integer> name2SvnV = new HashMap<>();               //文件名-最高svn版本号
        Map<String, Integer> nameBR2SvnV = new HashMap<>();                  //文件名+需求点组成的string-最高svn版本
        Map<String, Integer> name2SvnDelete = new HashMap<>();          //文件名-svn版本号
        
        String svnFile = "F:/daimagengxin.txt";
        
        String regEx1 = "Revision: \\d+";           // [0-9]+    \d
        String regEx2 = "\\d+\\.\\d+";              // 需求点
//        String regEx3 = "[^/]+$";                   // file name
//        String regEx3 = "[^/][\\w+-._]+$";
        String regEx3 = "[^/][a-zA-Z0-9_.-]+\\.(java|native|properties|xml|jsp)";
        String svnDel = "Deleted :";                // .
        
        String author = "Author: [^\n]+";
        String msg = "Message:\n[^\n]+";
        
        Pattern p1 = Pattern.compile(regEx1);
        Pattern p2 = Pattern.compile(regEx2);
        Pattern p3 = Pattern.compile(regEx3);
        
        Pattern p4 = Pattern.compile(author);
        Pattern p5 = Pattern.compile(msg);
        
        
        String temp = null;
        String name = null;
        String br = null;
        String nameBr = null;
        int svnV = 0;
        Matcher m = null;
        
        File svnF = new File(svnFile);
        try {
            BufferedReader reader = new BufferedReader(new FileReader(svnF));
            
            while ((temp = reader.readLine()) != null) {
                m = p3.matcher(temp);
                if (m.find()) {
                    name = m.group();
//                    System.out.println(name);
                    if (!name2SvnV.containsKey(name) || svnV > name2SvnV.get(name)) {
                        name2SvnV.put(name, svnV);
                    }

                    nameBr = name + " : " + br;
                    if (!nameBR2SvnV.containsKey(nameBr) || svnV > nameBR2SvnV.get(nameBr)) {
                        nameBR2SvnV.put(nameBr, svnV);
                    }

                    if (temp.startsWith(svnDel) && (!name2SvnDelete.containsKey(name) || svnV > name2SvnDelete.get(name))) {
                        name2SvnDelete.put(nameBr, svnV);
                    }
                    continue;
                }
                
                
                m = p2.matcher(temp);
                if(m.find())
                {
                    br = m.group();
//                    System.out.println(br);
                    continue;
                }
                
                m = p1.matcher(temp);
                if(m.find())
                {
                    //找到svn版本后，应该会找到需求点，如果有人没有写的话，那就把需求点==svn版本，看到后手动修改
                    svnV = Integer.parseInt(m.group().substring(10));
                    br = String.valueOf(svnV);
//                    System.out.println(svnV);
                    continue;
                }
                
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        
        
        //-----------------------------------
        System.out.println("name2SvnV size : " + name2SvnV.size());
        System.out.println("nameBR2SvnV size : " + nameBR2SvnV.size());
        System.out.println("nameBr2SvnDelete size : " + name2SvnDelete.size());
        
        
        String out1 = "F:/代码更新自动创建_格式1_" + new SimpleDateFormat("yyyy-MM-dd").format(new Date()) + "_" + new Date().getTime() / 1000 % 10000 + ".xlsx";
        
        XSSFWorkbook workbook = new XSSFWorkbook();
        XSSFSheet sh = workbook.createSheet();
        
        sh.setColumnWidth(2, 18000);
        sh.setColumnWidth(6, 18000);
        
        XSSFRow row = null;
        XSSFCell ce1 = null;
        XSSFCell ce2 = null;
        XSSFCell ce3 = null;
        
        XSSFCell ce4 = null;
        XSSFCell ce5 = null;
        
        String[] str = null;
        
        int i = 1;
        row = sh.createRow(i);
        ce1 = row.createCell(6);
        ce2 = row.createCell(7);
        ce1.setCellValue("受影响的文件数(没有剔除被删除的文件)要人为删除");
        ce2.setCellValue(name2SvnV.size());
        
//        i = 1;
//        row = sh.createRow(i);
        ce1 = row.createCell(2);
        ce1.setCellValue("文件在需求点中的最高版本(没有剔除被删除的文件)要人为删除");
        i += 2;
        
        row = sh.createRow(i);
        ce1 = row.createCell(2);
        ce1.setCellValue("需求点可能不对，如果svn注释没写的话，会用上一个svn版本的需求点");
        
        i += 2;
        for (Map.Entry<String, Integer> entry : nameBR2SvnV.entrySet()) {
            nameBr = entry.getKey();
            svnV = entry.getValue();
            
            str = nameBr.split(" : ");
//            System.out.println(nameBr + " : " + str.length + ", " + str[0] + ", " + str[1]);
            
            // 文件名，svn版本，需求点
            row = sh.createRow(i);
            ce1 = row.createCell(2);
            ce2 = row.createCell(3);
            ce3 = row.createCell(4);
            
            ce1.setCellValue(str[0]);
            ce2.setCellValue(svnV);
            ce3.setCellValue(str[1]);
            i += 1;
        }
        
        i += 1;
        row = sh.createRow(i++);
        ce1 = row.createCell(2);
        ce1.setCellValue("删除的文件,需求点和版本号，要人为确定后续没有又添加");
        for (Map.Entry<String, Integer> entry : name2SvnDelete.entrySet()) {
            nameBr = entry.getKey();
            svnV = entry.getValue();
            
            str = nameBr.split(" : ");
            
            row = sh.createRow(i);
            ce1 = row.createCell(2);
            ce2 = row.createCell(3);
            ce3 = row.createCell(4);
            
            ce1.setCellValue(str[0]);
            ce2.setCellValue(svnV);
            ce3.setCellValue(str[1]);
            i++;
        }
        
        i = 3;
        row = sh.getRow(i);
        ce1 = row.createCell(6);
        ce1.setCellValue("文件在整个需求中的最高版本(没有剔除被删除的文件)要人为删除");
        
//        System.out.println(ce1.getStringCellValue());
        
        i = 5;
        for (Map.Entry<String, Integer> entry : name2SvnV.entrySet()) {
            name = entry.getKey();
            svnV = entry.getValue();
            
            row = sh.getRow(i);
            ce4 = row.createCell(6);
            ce5 = row.createCell(7);
            
            ce4.setCellValue(name);
            ce5.setCellValue(svnV);
            i++;
        }
        
        FileOutputStream out = new FileOutputStream(out1);
        workbook.write(out);
        out.close();
        System.out.println("done");
        
//        row = sh.getRow(3);
//        ce1 = row.getCell(6);
//        System.out.println(ce1.getStringCellValue());
    }
    
}