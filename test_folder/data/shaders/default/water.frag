uniform sampler2D FieldSampler;
uniform float Cutoff;
uniform vec4 uColor;

varying vec2 vTC;

const float Wiggle = 0.15;

void main()
{
	vec4 tex = texture2D(FieldSampler, vTC);
	
	float meta = tex.b;
	
	float water  = smoothstep(Cutoff-Wiggle, Cutoff+Wiggle, meta);
	gl_FragColor = uColor;
	gl_FragColor.a *= water;
	
	float foam = abs(meta-Cutoff) / (Wiggle * 1.0);
	vec3 FoamColor = clamp(8.0 * uColor.rgb, 0.0, 1.0);
	gl_FragColor.rgb = mix(uColor.rgb, FoamColor, clamp(1.0-foam, 0.0, 1.0));
	
	float select = abs(tex.r-Cutoff) / (Wiggle * 2.0);
	gl_FragColor = mix(gl_FragColor, vec4(1.0), clamp(1.0-select, 0.0, 1.0));
}
