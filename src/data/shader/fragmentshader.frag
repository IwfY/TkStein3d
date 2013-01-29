#version 120

varying vec4 ex_color;
varying vec2 uv_pass;

void main() {
	vec4 black = vec4(0.0f, 0.0f, 0.0f, 1.0f);
	if (uv_pass.x > 0.995 || uv_pass.x < 0.005 || uv_pass.y > 0.995 || uv_pass.y < 0.005) {
		gl_FragColor = mix(ex_color, black, 0.2f);
	} else {
    	gl_FragColor = ex_color;
    }
}
