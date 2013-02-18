#version 120

varying vec4 ex_color;
varying vec2 uv_pass;
varying float squareDepth;

void main() {
	vec4 black = vec4(0.0f, 0.0f, 0.0f, 1.0f);
	vec4 tmp_color = ex_color;
	
	// fragment borders
	if (uv_pass.x > 0.995 || uv_pass.x < 0.005 || uv_pass.y > 0.995 || uv_pass.y < 0.005) {
		tmp_color = mix(tmp_color, black, 0.2f);
	}
	
	// make distant fragments darker
	float black_potion = squareDepth / 1000.0f;
    if (black_potion > 1.0f) {
        black_potion = 1.0f;
    }    
    tmp_color = mix(tmp_color, black, black_potion);
    
    // near surfaces bw
    /*
    if (squareDepth > 10.0f) {
    	float average = (tmp_color[0] + tmp_color[1] + tmp_color[2]) / 3.0f;
    	average += 0.3f;
    	if (average > 1.0f) {
    		average = 1.0f;
    	}
    	tmp_color = vec4(average, average, average, 1.0f);
    }
    
    if (squareDepth < 10.0f && squareDepth > 9.8f) {
    	float average = (tmp_color[0] + tmp_color[1] + tmp_color[2]) / 3.0f;
    	average -= 0.3f;
    	if (average < 0.0f) {
    		average = 0.0f;
    	}
    	tmp_color = vec4(average, average, average, 1.0f);
    }
    */
    
    gl_FragColor = tmp_color;
}
