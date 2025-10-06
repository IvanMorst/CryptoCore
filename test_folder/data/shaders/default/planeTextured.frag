varying vec2 vTC0;
varying vec2 vTC1;

///////////////////////////
// Common stuff
// Made for premultiplied alpha

uniform vec4   InsideColor;
uniform vec4   BorderColor;
uniform float  BorderWidth;
uniform float  PixelSize;
uniform sampler2D uTex;

float Smooth(float ps, float a)
{
	return clamp(a/ps+0.5, 0.0, 1.0);
}

vec4 CalcColor(float d)
{
	vec4 texColor = texture2D(uTex, vTC1);
	
	vec4 insideColor = InsideColor * texColor;
	vec4 borderColor = BorderColor;
		
	d = -d; // Invert, so that d is the depth into the body
	
	vec4 ret = mix(borderColor, insideColor, Smooth(PixelSize, d-BorderWidth));  // Border-inside AA
		
	return ret * Smooth(PixelSize, d); // Edge AA
}

//////////////////////////

uniform vec3 Plane;

void main()
{
	vec2 normal = Plane.xy;	
	float d = dot(vTC0, normal) + Plane.z;
	gl_FragColor = CalcColor(d);
}
