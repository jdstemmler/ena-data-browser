<html>

    <head>
        <title>ENA Data Browser</title>
        <link href="support-files/style.css" rel="stylesheet" type="text/css">
    </head>

    <body>
        <div class="container clearfix" id="plots">
            <?php
                $date = $_GET["date"];

                $current = date_create($date);

                $next = date_create($date);
                date_add($next, date_interval_create_from_date_string('1 days'));

                $prev = date_create($date);
                date_sub($prev, date_interval_create_from_date_string('1 days'));

                $main_plot = "support-files/figures/main/" . date_format($current, 'Y-m-d') . ".png";
                $rose_plot = "support-files/figures/rose/" . date_format($current, 'Y-m-d') . ".png";
                $aqua_plot = "http://lance-modis.eosdis.nasa.gov/imagery/subsets/tmp/ARM_Azores." . date_format($next,'Y') . str_pad(date_format($next, 'z'), 3, '0', STR_PAD_LEFT) . ".aqua.2km.jpg";
                $worldview = "https://worldview.earthdata.nasa.gov/?p=geographic&l=MODIS_Aqua_CorrectedReflectance_TrueColor,MODIS_Terra_CorrectedReflectance_TrueColor(hidden),MODIS_Aqua_CorrectedReflectance_Bands721(hidden),MODIS_Terra_CorrectedReflectance_Bands721(hidden),Calipso_Orbit_Asc,Coastlines,AMSR2_Cloud_Liquid_Water_Day(hidden),AMSR2_Cloud_Liquid_Water_Night(hidden),AMSR2_Wind_Speed_Day(hidden),AMSR2_Wind_Speed_Night(hidden)&t=" . date_format($current, 'Y-m-d') . "&v=-59.90624999999999,29.53125,-0.8437499999999929,61.9453125";
                $dl_aqua = "support-files/figures/satellite/" . date_format($current, 'Y-m-d') . ".png";
            ?>

            <header>
                <h1>ENA Data Browser</h1>
            </header>

            <?php require($DOCUMENT_ROOT . "support-files/navbar.php"); ?>

            <div class="main plot-page">
                <table>
                    <tr>
                        <td>
                            <!-- <img src="support-files/arrow_left.png"> -->
                            <form action="ena-figures.php" method="GET" name="ena-figures">
                                <input class="move-day" type="submit" name="date" value="<?php echo date_format($prev, 'Y-m-d'); ?>">
                            </form>
                        </td>
                        <td><?php echo "<h1>".date_format($current, 'Y-m-d')."</h1>"; ?></td>
                        <td>
                            <!-- <img src="support-files/arrow_right.png"> -->
                            <form action="ena-figures.php" method="GET" name="ena-figures">
                                <input class="move-day" type="submit" name="date" value="<?php echo date_format($next, 'Y-m-d'); ?>">
                            </form>
                        </td>
                    </tr>
                </table>

                <a href="<?php echo $main_plot; ?>" target="_blank">
                    <img id="main" src="<?php echo $main_plot; ?>">
                </a>
                <!--
                <a href="<?php echo $rose_plot; ?>">
                    <img id="rose" src="<?php echo $rose_plot; ?>">
                </a>
                -->
                <a href="<?php echo $worldview; ?>" target="_blank">
                    <img id="sat" src="<?php echo $dl_aqua; ?>" >
                </a>
            </div>
        </div>
    </body>
</html>
