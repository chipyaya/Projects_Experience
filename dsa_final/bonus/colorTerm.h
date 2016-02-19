#ifndef COLOR_TERM
#define COLOR_TERM

#include <cstdio>
enum COLOR
{ BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE };

inline void boldBegin(COLOR color){ printf("\x1b[1m[3%dm", color);}
inline void underlineBegin(COLOR color){ printf("\x1b[4m[3%dm", color);}
inline void foregroundBegin(COLOR color){ printf("\x1b[3%dm", color);}
inline void backgroundBegin(COLOR color){ printf("\x1b[4%dm", color); }
inline void syntaxEnd(){printf("[m");}
#endif
