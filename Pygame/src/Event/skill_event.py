import random
import pygame
import imp
import sys

from Event.base_event import BaseEvent
import Event.game_event
import Event.ui_event
import Event.io_event
from Event.animation_event import EventDrawSkillAnime, EventDrawEatNearAnime, EventDrawShoot
from player import Player
from helper import Helper
from gamemap import Map
import const as CON


class EventSkillDizzy( BaseEvent ):
    def __init__( self , env , priority , player_id ):
        self.env = env
        self.priority = priority
        self.pid = player_id
        self.cached_dir = [ None for i in range( 4 ) ]

    def do_action( self ):
        for i in range( 4 ):
            if i == self.pid:
                continue
            self.env[ "player" ][ i ].is_dizzy = True
            self.cached_dir[ i ] = self.env[ "player" ][ i ].dir[:]
            self.env[ "player" ][ i ].dir = ( 0 , 0 )
            #if self.env[ "player" ][ i ].dead:
            #    self.env[ "player" ][ i ].limit_time += CON.TICKS_PER_TURN * CON.TURNS_PER_MOVE * CON.DIZZY_TIME

        self.env[ "uic" ].add_event(
            EventDrawSkillAnime( self.env , self.priority + 1 , "Dizzy", self.pid )
        )

        self.env[ "gamec" ].add_event(
            EventSkillEndDizzy(
                self.env , self.priority + CON.TICKS_PER_TURN * CON.TURNS_PER_MOVE * CON.DIZZY_TIME , self.pid , self.cached_dir
            )
        )

class EventSkillEndDizzy( BaseEvent ):
    def __init__( self , env , priority , player_id , cached_dir ):
        self.env = env
        self.priority = priority
        self.pid = player_id
        self.cached_dir = cached_dir

    def do_action( self ):
        for i in range( 4 ):
            self.env[ "player" ][ i ].is_dizzy = False
            if i != self.pid:
                self.env[ "player" ][ i ].dir = self.cached_dir[ i ]

class EventSkillConfuse( BaseEvent ):
    def __init__( self , env , priority , player_id ):
        self.env = env
        self.priority = priority
        self.pid = player_id

    def do_action( self ):
        for i in range( 4 ):
            if i == self.pid:
                continue
            self.env[ "player" ][ i ].is_dizzy = True

        for i in range( CON.CONFUSE_TIME ):
            self.env[ "gamec" ].add_event(
                EventSkillConfusing( self.env , self.priority + CON.TICKS_PER_TURN * CON.TURNS_PER_MOVE * i , self.pid )
            )
        self.env[ "uic" ].add_event(
            EventDrawSkillAnime( self.env , self.priority + 1 , "Confuse", self.pid )
        )

        self.env[ "gamec" ].add_event(
            EventSkillEndConfuse(
                self.env , self.priority + CON.TICKS_PER_TURN * CON.TURNS_PER_MOVE * CON.CONFUSE_TIME , self.pid
            )
        )

class EventSkillConfusing( BaseEvent ):
    def __init__( self , env , priority , player_id ):
        self.env = env
        self.priority = priority
        self.player = env[ "player" ]
        self.pid = player_id

    def do_action( self ):
        dirs = [ ( -1 , 0 ) , ( 1 , 0 ) , ( 0 , -1 ) , ( 0 , 1 ) ]
        for i in range( 4 ):
            if i == self.pid or self.player[ i ].dead:
                continue
            self.player[ i ].dir = dirs[ random.randrange( 4 ) ]


class EventSkillEndConfuse( EventSkillEndDizzy ):
    def __init__( self , env , priority , player_id ):
        self.env = env
        self.priority = priority
        self.pid = player_id

    def do_action( self ):
        for i in range( 4 ):
            self.env[ "player" ][ i ].is_dizzy = False

class EventSkillBonus( BaseEvent ):
    def __init__( self , env , priority , player_id ):
        self.env = env
        self.priority = priority
        self.pid = player_id

    def do_action( self ):
        self.env[ "player" ][ self.pid ].score_rate = 2

        self.env[ "uic" ].add_event(
            EventDrawSkillAnime( self.env , self.priority + 1 , "Bonus", self.pid )
        )

        self.env[ "gamec" ].add_event(
            EventSkillEndBonus(
                self.env , self.priority + CON.TICKS_PER_TURN * CON.TURNS_PER_MOVE * CON.BONUS_TIME , self.pid
            )
        )

class EventSkillEndBonus( BaseEvent ):
    def __init__( self , env , priority , player_id ):
        self.env = env
        self.priority = priority
        self.pid = player_id

    def do_action( self ):
        self.env[ "player" ][ self.pid ].score_rate = 1

class EventSkillEatNear( BaseEvent ):
    def __init__( self , env , priority , player_id ):
        self.env = env
        self.priority = priority
        self.pid = player_id
        self.player = env[ "player" ][ self.pid ]
        self.foods = env[ "food" ]

    def do_action( self ):
        ( px , py ) = self.player.pos
        eaten_foods = []
        for ( fx , fy ) in self.foods:
            if abs( px - fx ) + abs( py - fy ) <= 4:
                eaten_foods.append( ( fx , fy ) )
        self.env[ "uic" ].add_event(
            EventDrawSkillAnime( self.env , self.priority + 1 , "Near", self.pid )
        )
        self.env[ "uic" ].add_event(
            EventDrawEatNearAnime( self.env , self.priority + 3 , self.pid , eaten_foods )
        )


class EventSkillShootYou(BaseEvent):
    def __init__(self, env, priority, playerid):
        self.env = env
        self.priority = priority
        self.pid = playerid
        self.player = env["player"][self.pid]
        self.players = env["player"]
    def do_action(self):
        (px, py) = self.player.pos
        highest_player = 0
        target_flag = False
        player_list = [0, 1, 2, 3]
        random.shuffle(player_list)
        for index in range(4):
            i = player_list[index]
            if self.pid == i or self.players[i].dead:
                continue
            if not target_flag:
                highest_player = i
                target_flag = True
            elif self.players[i].score > self.players[highest_player].score:
                highest_player = i
        self.env["uic"].add_event(
            EventDrawSkillAnime(self.env, self.priority + 1, "Shoot", self.pid)
        )
        if target_flag:
            self.env["uic"].add_event(
                EventDrawShoot(self.env, self.priority + 3, self.pid, highest_player)
            )
