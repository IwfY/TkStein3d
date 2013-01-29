#version 120

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
attribute vec4 in_color;
varying vec4 ex_color;

void main(void) {
    vec4 final_vertex = projection_matrix * view_matrix * gl_Vertex;
    gl_Position = final_vertex;
    
    float square_distance_vertex_player = final_vertex[0] * final_vertex[0] + final_vertex[1] * final_vertex[1] + final_vertex[2] * final_vertex[2];
                         
    float black_potion = square_distance_vertex_player / 1000.0f;
    if (black_potion > 1.0f) {
        black_potion = 1.0f;
    }
    
    vec4 black = vec4(0.0f, 0.0f, 0.0f, 1.0f);
    ex_color = mix(in_color, black, black_potion);
}
