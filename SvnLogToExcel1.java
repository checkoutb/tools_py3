

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
        
        Map<String, Integer> name2SvnV = new HashMap<>();               //�ļ���-���svn�汾��
        Map<String, Integer> nameBR2SvnV = new HashMap<>();                  //�ļ���+�������ɵ�string-���svn�汾
        Map<String, Integer> name2SvnDelete = new HashMap<>();          //�ļ���-svn�汾��
        
        String svnFile = "F:/daimagengxin.txt";
        
        String regEx1 = "Revision: \\d+";           // [0-9]+    \d
        String regEx2 = "\\d+\\.\\d+";              // �����
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
                    //�ҵ�svn�汾��Ӧ�û��ҵ�����㣬�������û��д�Ļ����ǾͰ������==svn�汾���������ֶ��޸�
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
        
        
        String out1 = "F:/��������Զ�����_��ʽ1_" + new SimpleDateFormat("yyyy-MM-dd").format(new Date()) + "_" + new Date().getTime() / 1000 % 10000 + ".xlsx";
        
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
        ce1.setCellValue("��Ӱ����ļ���(û���޳���ɾ�����ļ�)Ҫ��Ϊɾ��");
        ce2.setCellValue(name2SvnV.size());
        
//        i = 1;
//        row = sh.createRow(i);
        ce1 = row.createCell(2);
        ce1.setCellValue("�ļ���������е���߰汾(û���޳���ɾ�����ļ�)Ҫ��Ϊɾ��");
        i += 2;
        
        row = sh.createRow(i);
        ce1 = row.createCell(2);
        ce1.setCellValue("�������ܲ��ԣ����svnע��ûд�Ļ���������һ��svn�汾�������");
        
        i += 2;
        for (Map.Entry<String, Integer> entry : nameBR2SvnV.entrySet()) {
            nameBr = entry.getKey();
            svnV = entry.getValue();
            
            str = nameBr.split(" : ");
//            System.out.println(nameBr + " : " + str.length + ", " + str[0] + ", " + str[1]);
            
            // �ļ�����svn�汾�������
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
        ce1.setCellValue("ɾ�����ļ�,�����Ͱ汾�ţ�Ҫ��Ϊȷ������û�������");
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
        ce1.setCellValue("�ļ������������е���߰汾(û���޳���ɾ�����ļ�)Ҫ��Ϊɾ��");
        
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