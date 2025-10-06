///////////////////////////
// Common stuff
// Made for premultiplied alpha

uniform vec4   InsideColor;
uniform vec4   BorderColor;
uniform float  BorderWidth;
uniform float  PixelSize;

float Smooth(float ps, float a)
{
	return clamp(a/ps+0.5, 0.0, 1.0);
}

vec4 CalcColor(float d)
{	
	d = -d; // Invert, so that d is the depth into the body
	
	vec4 ret = mix(BorderColor, InsideColor, Smooth(PixelSize, d-BorderWidth));  // Border-inside AA
	
	return ret * Smooth(PixelSize, d); // Edge AA
}

//////////////////////////

uniform vec3 Plane;

varying vec2 vTC;

void main()
{
	vec2 normal = Plane.xy;	
	float d = dot(vTC, normal) + Plane.z;	
	gl_FragColor = CalcColor(d);
}
