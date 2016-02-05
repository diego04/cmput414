// Your loader is implemented in this file


// Global var definition (e.g.:  camera, scene, mesh, etc. )
var camera, scene;


// Your Methods 


/** Switch between solid and wireframe modes */
function switch_display() 
{

}

/** Initialize Three.js objs */
function initialize()
{
	container = document.getElementById("webgl");
	var width = container.clientWidth;
	var height = container.clientHeight;

	// Create camera and move it along the z-axis
	camera = new THREE.PerspectiveCamera(45,width/height,0.1,10000);
	camera.position.z = 500;

	scene = new THREE.Scene();

	// Continue it here ...	
}


/** Called when page is loaded */
function load()
{
	initialize();
	render();
}

