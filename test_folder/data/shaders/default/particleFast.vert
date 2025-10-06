uniform mat4 uMVP;

attribute vec2 aVert;
attribute vec2 aTC;

varying vec2 vTC;

void main()
{
	gl_Position = vec4(aVert, 0, 1);
	vTC = aTC;
} 
