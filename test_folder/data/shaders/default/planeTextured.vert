uniform mat4 uMVP;
uniform mat3 uTexMatrix;

attribute vec2 aVert;
attribute vec2 aTC;

varying vec2 vTC0;
varying vec2 vTC1;

void main()
{
	gl_Position = uMVP * vec4(aVert, 0, 1);
	vTC0 = aTC;
	vTC1 = (uTexMatrix * vec3(aTC, 1)).xy;
} 
