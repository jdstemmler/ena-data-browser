<html>
    <head>
        <title>ENA Data Browser</title>
        <link href="support-files/style.css" rel="stylesheet" type="text/css">
    </head>
    
    <body>
        <div class="container clearfix">
            <?php 
            $linkstr = '<a href="ena-figures.php?date='
            ?>
            <header><h1>ENA Data Browser</h1></header>
            
            <?php require($DOCUMENT_ROOT . "support-files/navbar.php"); ?>
            <div class="main">
                <h2>Interesting Cases</h2>
                <p>Main body content here</p>
                
                <table class="cases">
                    <tr>
                        <th class="left">Date</th>
                        <th class="right">Description</th>
                    </tr>
                    
                    <?php
                        include "support-files/cases.php";
                        foreach ($cases as $d => $description) {
                            echo "<tr>";
                            echo "<td>";
                            echo "<a href='ena-figures.php?date=$d'>$d</a>";
                            echo "</td>";
                            echo "<td>$description</td>";
                            echo "</tr>";
                        }
                    ?>
                    
                </table>
                
            </div>
        </div>
    </body>
</html>
