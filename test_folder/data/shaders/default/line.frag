varying vec2 vTC;
varying vec4 vColor;

uniform float uPixelSize;
uniform float uFadeWidth; // 0 for nice AA, 1 for very fuzzy line.

void main()
{
	gl_FragColor = vColor;
	vec2 tc = vTC;
	float x = tc.x;
	float width = tc.y;
	
	float fw = max(uPixelSize, width*uFadeWidth*0.5);
	
	float a = 1.0;
	
	a = min(x/fw, (width-x)/fw);
	a = clamp(a, 0.0, 1.0);
		
	// Fade out very thin lines
	a *= clamp(width/(2.0*uPixelSize), 0.0, 1.0);
		
	gl_FragColor.a *= a;
}
