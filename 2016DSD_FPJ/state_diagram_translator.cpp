#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include "quine_mc_cluskey.hpp"

#define SR 0
#define JK 1
#define D 2
#define T 3

#define d (-1)

using namespace std;

int excitation_SR[2][4] = {{0, 1, 0, d}, {d, 0, 1, 0}};
int excitation_JK[2][4] = {{0, 1, d, d}, {d, d, 1, 0}};
int excitation_D[4] = {0, 1, 0, 1};
int excitation_T[4] = {0, 1, 1, 0};

/* data structure for Quine_McCluskey, implemented by Stefan Moebius. */
int prim[MAX];
int prim_mask[MAX];
int prim_required[MAX] = {0};
int prim_cnt = 0;
int terms_dont_care[MAX] = {0};

int terms_out[MAX][MAX];
int num_terms_out = 0;

int num_terms_ff = 0;
int terms_ff[MAX][MAX];

int getFFId(string s) {
    if(s == "R")	//RS
        return SR;
    if(s == "J")	//JK
        return JK;
    if(s == "D")
        return D;
    if(s == "T")
        return T;

    cout << "error: no such ff_type." << endl;
    exit(-1);
}

int excitation(int ff_type, int transition, int param) {
    if(ff_type == SR)
        return excitation_SR[param][transition];
    if(ff_type == JK)
        return excitation_JK[param][transition];
    if(ff_type == D)
        return excitation_D[transition];
    if(ff_type == T)
        return excitation_T[transition];

    cout << "error: no such ff_type." << endl;
    exit(-1);
}

void printTerms(int* prim, int* prim_mask, int* prim_required, int prim_cnt, int num_var) {
    //bool space_flag = false;

    for(int i = 0; i < prim_cnt; i++) {
        if(prim_required[i]) {
			/*
            if(space_flag)
                cout << " ";
            space_flag = true;
			*/
            for(int s = num_var - 1; s >= 0; s--) {
                if((prim_mask[i] & (1 << s)) == 0)
                    cout << 2;
                else {
                    if(prim[i] & (1 << s))
                        cout << 1;
                    else
                        cout << 0;
                }
            }
        }
    }
}

void printFFType(int ff_type) {
    string type_strings[] = {"RS", "JK", "D", "T"};
    cout << type_strings[ff_type] << endl;
}


int main(int argc, char *argv[]) {
    /* read inputs. */

    int N;

    int num_input = stoi(argv[2]);
    int num_state = stoi(argv[1]);

    //cin >> num_state >> num_input;

    string ff_type_s;
    int ff_types[MAXVARS];

    for(int i = num_state - 1; i >= 0; i--) {
		ff_type_s = argv[3+num_state - 1 - i];
        //cin >> ff_type_s;
        ff_types[i] = getFFId(ff_type_s);
    }
    
    N = (1 << (num_input + num_state));

    int state_transition[MAX]; 

    for(int i = 0; i < N; i++) {
		int start = 3+num_state;
        int this_state_input = stoi(argv[start+i*3]);
		int next_state = stoi(argv[start+1+i*3]);
		int output = stoi(argv[start+2+i*3]);

        //cin >> this_state_input >> next_state >> output;

        if(output) {
            terms_out[num_terms_out++][0] = i;
        }
        state_transition[this_state_input] = next_state;
    }

    cout << num_state << endl << num_input << endl;
    
    /* simplified the output expression. */
    Quine_McCluskey(num_state + num_input, num_terms_out, terms_out, terms_dont_care, prim, prim_mask, prim_required, prim_cnt);
    
    /* print output terms. */
    printTerms(prim, prim_mask, prim_required, prim_cnt, num_state + num_input);
    cout << endl;


    /* TODO: Modified this part. Enable different states can be implemented by different FFs. */
    /* deal with the state expression. */
    for(int s = num_state - 1; s >= 0; s--) {
        int num_params = ((ff_types[s] == SR || ff_types[s] == JK) ? 2 : 1); 
        printFFType(ff_types[s]);
        for(int param = 0; param < num_params; param++) {
            num_terms_ff = 0;
            memset(terms_dont_care, FALSE, MAX * sizeof(int));
            for(int i = 0; i < N; i++) {
                bool now = ((i & (1 << (s + num_input))) != 0);
                bool next = ((state_transition[i] & (1 << s)) != 0);

                int transition = (now ? 2 : 0) + (next ? 1 : 0);

                int e = excitation(ff_types[s], transition, param);
                
                if(e != 0)
                    terms_ff[num_terms_ff++][0] = i;

                if(e == d) {
                    terms_dont_care[i] = TRUE;
                }
            }

            /* simplified the state expression. */
            Quine_McCluskey(num_state + num_input, num_terms_ff, terms_ff, terms_dont_care, prim, prim_mask, prim_required, prim_cnt);
            
            /* print state terms. */
            printTerms(prim, prim_mask, prim_required, prim_cnt, num_state + num_input);
            //if(!(s == 0 && param == num_params - 1))
                cout << endl;
        }
    }
}
