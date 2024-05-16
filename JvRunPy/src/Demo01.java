import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Demo01 {
    public static void main(String[] args) throws IOException, InterruptedException {
        // TODO Auto-generated method stub
//        get_stock_price("2017-01-01", "2023-04-29");
//        get_stock_enterprise();
//        get_stock_heat();
//        get_stock_realtime_data("SZ000010");
//        String[] data_array = get_stock_realtime_data("SZ000001");

        Boolean res = stock_data_predict();
        System.out.println("[RES] "+ res);
    }

    public static Boolean stock_data_predict() {
        try {
            System.out.println("[Python] \"update_stock_data_file\":start");
            /*下面这行String里的数组很关键，它有两个参数，都推荐使用绝对路径，
            第一个参数是你python编译器所在的位置，直接写python，系统会使用默认的python，
            第二个参数是你python文件所在的位置。
            */
            String[] arg = new String[]{"python", "C:\\Users\\Fm\\Desktop\\code\\Py\\pythonProj_4_12\\venv\\shares.py"};
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));

            String line;
            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
                System.out.println(line);
            }
            in.close();

            // 结束
            System.out.println("[Python] \"update_stock_data_file\":end");

            pr.waitFor();
            InputStream errorStream = pr.getErrorStream();
            BufferedReader error = new BufferedReader(new InputStreamReader(errorStream, "gbk"));

            String lines;
            Boolean if_not_error = true;
            while ((lines = error.readLine()) != null) {
                System.out.println("[PythonError]" + lines);

                if_not_error = false;
            }
            error.close();

            return if_not_error;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return false;
    }


    // 返回一个字符串数组，分别包含 现价 涨幅（值） 涨幅（百分比）
    public static String[] get_stock_realtime_data(String stock_id) throws IOException, InterruptedException {
        try {
            System.out.println("[Python] \"get_stock_realtime_data\":start");
            /*下面这行String里的数组很关键，它有两个参数，都推荐使用绝对路径，
            第一个参数是你python编译器所在的位置，直接写python，系统会使用默认的python，
            第二个参数是你python文件所在的位置。
            */
            String[] arg = new String[]{"python", "PythonExec/StockRealTimeData.py", stock_id};
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));

            String res = "null";

            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                res = line;
            }
            in.close();

            // 结束
            System.out.println("[Python] \"get_stock_realtime_data\":start");

            pr.waitFor();
            InputStream errorStream = pr.getErrorStream();
            BufferedReader error = new BufferedReader(new InputStreamReader(errorStream, "gbk"));

            String lines;
            while ((lines = error.readLine()) != null) {
                System.out.println("[Python]" + lines);
            }
            error.close();

            return res.split(",");
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new String[]{};
    }

    public static void get_stock_data() {
//        try {
//            String[] args1 = new String[] { "python", "PythonExec/StockDataGet.py"};
//            Process proc = Runtime.getRuntime().exec(args1);// 执行py文件
//
//            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
//            String line = null;
//            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
//                System.out.println("[Python] " + line);
//            }
//            in.close();
//            proc.waitFor();
//        } catch (IOException | InterruptedException e) {
//            e.printStackTrace();
//        }

        try {
            System.out.println("[Python] \"get_stock_data\":start");
            /*下面这行String里的数组很关键，它有两个参数，都推荐使用绝对路径，
            第一个参数是你python编译器所在的位置，直接写python，系统会使用默认的python，
            第二个参数是你python文件所在的位置。
            */
            String[] arg = new String[]{"python", "PythonExec/StockDataGet.py"};
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));

            String line;
            while ((line = in.readLine()) != null) {
                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
                    continue;
                System.out.println(line);
            }
            in.close();

            // 结束
            System.out.println("[Python] \"get_stock_data\":end");

            pr.waitFor();
            InputStream errorStream = pr.getErrorStream();
            BufferedReader error = new BufferedReader(new InputStreamReader(errorStream, "gbk"));

            String lines;
            while ((lines = error.readLine()) != null) {
                System.out.println("[Python]" + lines);
            }
            error.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void get_stock_enterprise() {
//        try {
//            String[] args1 = new String[] { "python", "PythonExec/StockEnterpriseGet.py"};
//            Process proc = Runtime.getRuntime().exec(args1);// 执行py文件
//
//            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
//            String line = null;
//            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
//                System.out.println("[Python] " + line);
//            }
//            in.close();
//            proc.waitFor();
//        } catch (IOException | InterruptedException e) {
//            e.printStackTrace();
//        }


        try {
            System.out.println("[Python] \"get_stock_enterprise\":start");
            /*下面这行String里的数组很关键，它有两个参数，都推荐使用绝对路径，
            第一个参数是你python编译器所在的位置，直接写python，系统会使用默认的python，
            第二个参数是你python文件所在的位置。
            */
            String[] arg = new String[]{"python", "PythonExec/StockEnterpriseGet.py"};
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));

            String line;
            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
                System.out.println("[Python]" + line);
            }
            in.close();

            // 结束
            System.out.println("[Python] \"get_stock_enterprise\":end");

            pr.waitFor();
            InputStream errorStream = pr.getErrorStream();
            BufferedReader error = new BufferedReader(new InputStreamReader(errorStream, "gbk"));

            String lines;
            while ((lines = error.readLine()) != null) {
                System.out.println("[Python]" + lines);
            }
            error.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void get_stock_heat() {
//        try {
//            String[] args1 = new String[] { "python", "PythonExec/StockHeatGet.py"};
//            Process proc = Runtime.getRuntime().exec(args1);// 执行py文件
//
//            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
//            String line = null;
//            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
//                System.out.println("[Python] " + line);
//            }
//            in.close();
//            proc.waitFor();
//        } catch (IOException | InterruptedException e) {
//            e.printStackTrace();
//        }

        try {
            System.out.println("[Python] \"get_stock_heat\":start");
            /*下面这行String里的数组很关键，它有两个参数，都推荐使用绝对路径，
            第一个参数是你python编译器所在的位置，直接写python，系统会使用默认的python，
            第二个参数是你python文件所在的位置。
            */
            String[] arg = new String[]{"python", "PythonExec/StockHeatGet.py"};
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));

            String line;
            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
                System.out.println("[Python]" + line);
            }
            in.close();

            // 结束
            System.out.println("[Python] \"get_stock_heat\":end");

            pr.waitFor();
            InputStream errorStream = pr.getErrorStream();
            BufferedReader error = new BufferedReader(new InputStreamReader(errorStream, "gbk"));

            String lines;
            while ((lines = error.readLine()) != null) {
                System.out.println("[Python]" + lines);
            }
            error.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void get_stock_news() {
//        try {
//            String[] args1 = new String[] { "python", "PythonExec/StockNewsGet.py"};
//            Process proc = Runtime.getRuntime().exec(args1);// 执行py文件
//
//            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
//            String line = null;
//            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
//                System.out.println("[Python] " + line);
//            }
//            in.close();
//            proc.waitFor();
//        } catch (IOException | InterruptedException e) {
//            e.printStackTrace();
//        }

        try {
            System.out.println("[Python] \"get_stock_news\":start");
            /*下面这行String里的数组很关键，它有两个参数，都推荐使用绝对路径，
            第一个参数是你python编译器所在的位置，直接写python，系统会使用默认的python，
            第二个参数是你python文件所在的位置。
            */
            String[] arg = new String[]{"python", "PythonExec/StockNewsGet.py"};
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));

            String line;
            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
                System.out.println("Python" + line);
            }
            in.close();

            // 结束
            System.out.println("[Python] \"get_stock_news\":end");

            pr.waitFor();
            InputStream errorStream = pr.getErrorStream();
            BufferedReader error = new BufferedReader(new InputStreamReader(errorStream, "gbk"));

            String lines;
            while ((lines = error.readLine()) != null) {
                System.out.println("[Python]" + lines);
            }
            error.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 参数date_start、date_end的形式为 yyyy-mm-dd
    public static void get_stock_price(String date_start, String date_end) {
//        try {
//            String[] args1 = new String[] { "python", "PythonExec/StockPriceGet.py", date_start, date_end};
//            Process proc = Runtime.getRuntime().exec(args1);// 执行py文件
//
//            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
//            String line = null;
//            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
//                System.out.println("[Python] " + line);
//            }
//            in.close();
//            proc.waitFor();
//        } catch (IOException | InterruptedException e) {
//            e.printStackTrace();
//        }


        try {
            System.out.println("[Python] \"get_stock_price\":start");
            /*下面这行String里的数组很关键，它有两个参数，都推荐使用绝对路径，
            第一个参数是你python编译器所在的位置，直接写python，系统会使用默认的python，
            第二个参数是你python文件所在的位置。
            */
            String[] arg = new String[]{"python", "PythonExec/StockPriceGet.py", date_start, date_end};
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));

            String line;
            while ((line = in.readLine()) != null) {
//                if (line.length() >= 7 && line.substring(0, 7).equals("process"))
//                    continue;
                System.out.println("[Python]" + line);
            }
            in.close();

            // 结束
            System.out.println("[Python] \"get_stock_price\":end");

            pr.waitFor();
            InputStream errorStream = pr.getErrorStream();
            BufferedReader error = new BufferedReader(new InputStreamReader(errorStream, "gbk"));

            String lines;
            while ((lines = error.readLine()) != null) {
                System.out.println("[Python]" + lines);
            }
            error.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}