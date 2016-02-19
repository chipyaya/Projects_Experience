/*
 * This code was written by Kirk J. Krauss, and was not wriiten by our team.
 * Ref: www.drdobbs.com/architecture-and-design/matching-wildcards-an-empirical-way-to-t/240169123
 */
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
