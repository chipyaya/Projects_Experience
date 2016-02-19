#ifndef WILDCARD
#define WILDCARD

// This function compares text strings, one of which can have wildcards 
// ('*' or '?').
//
bool WildTextCompare(
    char *pTameText,   // A string without wildcards
    char *pWildText    // A (potentially) corresponding string with wildcards
);

#endif
