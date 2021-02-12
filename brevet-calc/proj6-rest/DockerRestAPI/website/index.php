<html>
    <head>
        <title>CIS 322 REST-api demo: Laptop list</title>
    </head>

    <body>
        <h1>List of Times</h1>
        <ul>
	    <?php
            echo "All Times";
            $json = file_get_contents('http://laptop-service/listAll');
            $obj = json_decode($json);
	          $times = $obj->Times;
            foreach ($times as $t) {
                echo "<li>$t</li>";
	    }
	    echo "<br>";
	    echo "Open Times Only";
            $json = file_get_contents('http://laptop-service/listOpenOnly');
            $obj = json_decode($json);
	          $times = $obj->Times;
            foreach ($times as $t) {
                echo "<li>$t</li>";
            }
	    echo "<br>";
	    echo "Close Times Only";
            $json = file_get_contents('http://laptop-service/listCloseOnly');
            $obj = json_decode($json);
	          $times = $obj->Times;
            foreach ($times as $t) {
                echo "<li>$t</li>";
            }
            ?>
        </ul>
    </body>
</html>
