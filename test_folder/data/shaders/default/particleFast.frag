uniform sampler2D uTex;

varying vec2 vTC;

void main()
{
	gl_FragColor = texture2D(uTex, vTC);
}
