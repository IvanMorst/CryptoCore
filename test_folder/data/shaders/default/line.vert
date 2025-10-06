uniform mat4 uMVP;

attribute vec2 aVert;
attribute vec2 aTC;
attribute vec4 aColor;

varying vec2 vTC;
varying vec4 vColor;

void main()
{
	gl_Position = uMVP * vec4(aVert, 0, 1);
	vTC = aTC;
	vColor = aColor;
} 
