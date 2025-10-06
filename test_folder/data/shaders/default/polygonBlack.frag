uniform sampler2D DistSampler;
varying vec2 vTC;

void main()
{
	float d = texture2D(DistSampler, vTC).a; // distance
	gl_FragColor.rgb = vec3(0.0);            // black
	gl_FragColor.a = step(-0.5, -d);         // 0.0 when d>0.5, else 1.0
}
