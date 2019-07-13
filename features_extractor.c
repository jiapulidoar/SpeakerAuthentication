// Voice Features extractor 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tensorflow/tensorflow/c/c_api.h>
  
char * _model_dir = "./Model/graph.pb"; 

TF_Buffer* read_file(const char* file ); 

void free_buffer(void * data, size_t length) {
  free(data);
}

void tensor_free_none(void * data, size_t len, void* arg) {
    //free(data);
}

typedef struct header_file
{
    char chunk_id[4];
    int chunk_size;
    char format[4];
    char subchunk1_id[4];
    int subchunk1_size;
    short int audio_format;
    short int num_channels;
    int sample_rate;                  // sample_rate denotes the sampling rate.
    int byte_rate;
    short int block_align;
    uint16_t bits_per_sample;
    char subchunk2_id[4];
    uint32_t subchunk2_size;                  // subchunk2_size denotes the number of samples.
} header;

typedef struct header_file* header_p;

int get_nframes( header_p  wave ){
    printf("sample_rate %i", wave -> sample_rate );
    int Num_frames = (wave -> subchunk2_size)/(wave ->bits_per_sample/8);
    return Num_frames;
}
void get_frames( FILE * fich, header_p head , short int * buff8){
   
    
    int num_frames = get_nframes(head);
    printf("numframes %i ",num_frames);
    
    int BUFFSIZE = num_frames ;
    
    printf("buffpf %li ",sizeof(buff8));

    //FILE *out; 
    //out  = fopen("wave.txt" , "w");
    
    if (fich){
        
        int nb = fread(buff8,sizeof(short int),BUFFSIZE,fich);
   
        //for (int j= 0;j< BUFFSIZE;j++){
        //    fprintf( out , "%i ", buff8[j]  );
        //}
         
    }

}


int main( int argc, char ** argv) {
    
    // Get wave 
    
    int num_frames = 0;
    FILE *fich;
    short int * wave_frames;
    
    fich = fopen( argv[1], "r");
    
    // save the information of the wave 
    header_p wave = (header_p)malloc(sizeof(header));
    fread( wave, 1 , sizeof(header) , fich  ); 
    num_frames = get_nframes(wave);
    wave_frames = (short int * ) malloc(sizeof(short int )*num_frames );
    
    get_frames( fich, wave , wave_frames); 
    
    float  floatdata [num_frames];
    
    for(int j =0; j<num_frames ; j++){
        floatdata[j] = (float) wave_frames[j];
    }
      printf("\n");
    for(int j =0; j<128 ; j++){
        printf("%f ", floatdata[j] );
    }
    
      printf("TensorFlow C library version: %s\n", TF_Version());
    
    TF_Buffer* graph_def = read_file(_model_dir);
 
      TF_Graph * graph = TF_NewGraph();
    TF_ImportGraphDefOptions* opts = TF_NewImportGraphDefOptions();
      TF_SessionOptions * options = TF_NewSessionOptions();
      TF_Status * status = TF_NewStatus();
      TF_Session * session = TF_NewSession(graph, options, status);
    TF_GraphImportGraphDef(graph, graph_def, opts, status);
    
    //if(TF_GetCode(status) != TF_OK) {
     //   fprintf(stderr, "ERROR: Unable to import graph %s", TF_Message(status));        
     //   return 1;
    //}
    
    size_t pos = 0;
    TF_Operation* oper;
    //while ((oper = TF_GraphNextOperation(graph, &pos)) != NULL) {
    //    printf("%s \n", TF_OperationName(oper));   
    //}
    
    
    TF_Operation  * input_1   = { TF_GraphOperationByName(graph, "input_1")} ;
    if(input_1 == NULL) { 
        printf("Failed to load 'input_1' \n");
        return(1);
    }
    TF_Operation  * ouput   = { TF_GraphOperationByName(graph, "strided_conv/add")} ;
    
    
    if(ouput == NULL) { 
        printf("Failed to load 'code' \n");
        return(2);
    }
    
    int64_t dims[] = {1,num_frames,1};
    int64_t num_dims = 3;
    
    TF_Tensor * tensor_in = TF_NewTensor(TF_FLOAT, dims, num_dims, floatdata, sizeof(float)*num_frames, tensor_free_none, NULL);
    
    TF_Tensor * tensor_out = NULL;
    
    
    TF_Output input_operations[] =  { input_1, 0};
      TF_Tensor ** input_tensors = { &tensor_in};

    TF_Output output_operations[] = { ouput, 0 };
      TF_Tensor ** output_tensors = { &tensor_out};
    
    TF_SessionRun(session, NULL,
                  // Inputs
                  input_operations, input_tensors, 1,
                  // Outputs
                  output_operations, output_tensors, 1,
                  // Target operations
                  NULL, 0, NULL,
                  status);
    
    if(tensor_out == NULL){
        printf("error calculate ");
        return 0 ;
    }
    
    printf("Session Run Status: %d - %s\n", TF_GetCode(status), TF_Message(status) );
    printf("Output Tensor Type: %d \n", (int)TF_Dim(tensor_out, 0));
    float * outval = TF_TensorData(tensor_out);

    for(int j =0; j<128 ; j++){
        printf("%f ", outval[j] );
    }

    FILE *out; 
    out  = fopen("./tmp/features.data" , "wb");
    fwrite(outval, sizeof(float), 128, out);
   
    fclose(out);
    
    TF_CloseSession(session, status);
      TF_DeleteSession(session, status);
 
      TF_DeleteSessionOptions(options);
 
      TF_DeleteGraph(graph);
 
      TF_DeleteTensor(tensor_in);
      TF_DeleteTensor(tensor_out);

 
      TF_DeleteStatus(status);
      return 0;
}


TF_Buffer* read_file(const char* file) {                                                  
  FILE *f = fopen(file, "rb");
  fseek(f, 0, SEEK_END);
  long fsize = ftell(f);                                                                  
  fseek(f, 0, SEEK_SET);  //same as rewind(f);                                            

  void* data = malloc(fsize);                                                             
  fread(data, fsize, 1, f);
  fclose(f);

  TF_Buffer* buf = TF_NewBuffer();                                                        
  buf->data = data;
  buf->length = fsize;                                                                    
  buf->data_deallocator = free_buffer;                                                    
  return buf;
} 








/*


 size_t pos = 0;
    TF_Operation* oper;
    while ((oper = TF_GraphNextOperation(graph, &pos)) != NULL) {
        printf("%s \n", TF_OperationName(oper));   
    }

*/
