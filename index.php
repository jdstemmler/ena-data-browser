<html>
    <head>
        <title>ENA Data Browser</title>
        <link href="support-files/style.css" rel="stylesheet" type="text/css">
    </head>
    
    <body>
        <div class="container clearfix">
            
            <header><h1>ENA Data Browser</h1></header>
            
            <?php require($DOCUMENT_ROOT . "support-files/navbar.php"); ?>
            <div class="main">
                <p>
                    Welcome to the data browser for the Atmospheric Radiation Measurement's 
                    Eastern North Atlantic permanent site. This site is created and maintained
                    by Jayson Stemmler of the University of Washington 
                    (<a href="mailto:jstemm@uw.edu">jstemm@uw.edu</a>). You should send him any
                    questions or issues you have, not ARM.
                </p>

                <h2>How to use this site</h2>

                <p>
                    This site provides quick and easy access to a number of data products from the
                    permanent ARM site in the ENA. The data used in the visualizations were downloaded
                    from the ARM Data Archive, which can be accessed through the "Order ENA Data" in
                    the navigation menu.
                </p>

                <p>
                    To begin, input a date into the field below and hit submit. At the moment, the plots
                    are static .png files which link to their full-sized versions. I am working on making
                    some more interactive plots for a future version.
                </p>
            
                <div class="form">
                    <form action="ena-figures.php" method="GET" name="ena-figures">
                        <!-- <input type="date" name="date" value="<?php echo date('Y-m-d'); ?>"> -->
                        <input type="date" name="date" value="2013-10-04">
                        <input type="submit" value="Submit">
                    </form>

                </div>
            
            </div>
        
        </div>
    
    </body>
</html>