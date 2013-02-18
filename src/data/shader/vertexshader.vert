#version 120

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
attribute vec4 in_color;
attribute vec2 uv;
varying vec4 ex_color;
varying vec2 uv_pass;
varying float squareDepth;

void main(void) {
    vec4 final_vertex = projection_matrix * view_matrix * gl_Vertex;
    gl_Position = final_vertex;
    
    squareDepth = final_vertex[0] * final_vertex[0] + final_vertex[1] * final_vertex[1] + final_vertex[2] * final_vertex[2];
    ex_color = in_color;
    uv_pass = uv;
}
