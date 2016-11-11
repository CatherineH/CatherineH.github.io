window.onload = function(){
    var s = Snap("#svg");
    var monitor_width_screen = 273;
    var monitor_height_screen = 240;
    var sketch_width = 600;

    var image_x = 80;
	var image_y = 24;

/*
    var monitor_width = 450;
    var monitor_width_screen = monitor_width*0.8;
    var monitor_curvature = 5;
    var computer_curvature = 5;
    var margin = 8;
	var sketch_width = 630-2*margin;
	var sketch_height = 600-3*margin;
    console.log("hello: ", sketch_width, margin);
	var old_plastic = {
        fill: "#dcddd0",
        stroke: "#000",
        strokeWidth: 3
    }
    var border = {
        fill: "none",
        stroke: "#000",
        strokeWidth: 3
    }
	var computer = s.rect(margin, monitor_width+margin*2, width=sketch_width,
	                      height=sketch_height-monitor_width,
	                      rx=computer_curvature, ry=computer_curvature);
	computer.attr(old_plastic);
	console.log("hello: ", sketch_width, margin);

	//monitor_width+(width-monitor_width)/2
	var monitor_x = margin+(sketch_width-monitor_width)/2;
	var monitor_y = margin;
	var monitor = s.rect(monitor_x, monitor_y,
	                     width=monitor_width,
	                     height=monitor_width, rx=monitor_curvature,
	                     ry=monitor_curvature);
    console.log("hello: ", sketch_width, margin);

	monitor.attr(old_plastic);
	s.path.difference()

    var trace2 = s.circle(monitor_x, monitor_y, 5, 5);
    console.log(sketch_width, margin, monitor_width, monitor_width_screen, image_x, monitor_x);
    monitor_image.attr(old_plastic);
*/
    var trace = s.circle(image_x, image_y, 5, 5);
    var turbo_image = "assets/images/running_face.jpg";
    var normal_image = "assets/images/professional.jpg";
    var off_image = "assets/images/off_screen.png";
    var screen_image = normal_image;
    var monitor_image = s.image(screen_image,
                                image_x,
                                image_y,
                                width=monitor_width_screen,
                                height=monitor_height_screen
                                );
    var clickCallback = function(event) {
        if(this.node.id == "reset")
        {
            screen_image = normal_image;
        }
        else if(this.node.id == "turbo")
        {
            screen_image = turbo_image;
        }
        else if(this.node.id == "off")
        {
            screen_image = off_image;
        }
        monitor_image = s.image(screen_image,
                                image_x,
                                image_y,
                                width=monitor_width_screen,
                                height=monitor_height_screen
                                );
        Snap.load("assets/images/computer.svg", load);
        this.attr({ fill: 'blue' });
    };


    function load(f)
    {
        g = f.select("g");
        turbo_button = g.select("#turbo");
        reset_button = g.select("#reset");
        off_button = g.select("#off");
        turbo_button.click(clickCallback);
        reset_button.click(clickCallback);
        off_button.click(clickCallback);
        s.append(g);
    }

    Snap.load("assets/images/computer.svg", load);
}
