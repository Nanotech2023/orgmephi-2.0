import { Component, OnInit } from '@angular/core'
import { footerHeight } from '@/shared/consts'
import { Observable } from 'rxjs'
import { animate, query, stagger, state, style, transition, trigger } from '@angular/animations'
import { ManageOlympiadsStore } from '@/manage-olympiads/manage-olympiads.store'
import { Contest } from '@api/tasks/model'


export const fadeAnimation = trigger( 'fadeAnimation', [
    transition( ':enter', [
            style( { opacity: 0 } ), animate( '300ms', style( { opacity: 1 } ) )
        ]
    ),
    transition( ':leave',
        [ style( { opacity: 1 } ), animate( '300ms', style( { opacity: 0 } ) ) ]
    )
] )

export const listAnimation = trigger( 'listAnimation', [
    transition( '* <=> *', [
        query( ':enter',
            [ style( { opacity: 0 } ), stagger( '60ms', animate( '600ms ease-out', style( { opacity: 1 } ) ) ) ],
            { optional: true }
        ),
        query( ':leave',
            animate( '300ms', style( { opacity: 0 } ) ),
            { optional: true }
        )
    ] )
] )

export const rotatedState = trigger( 'rotatedState', [
    state( 'true', style( { transform: 'rotate(0)' } ) ),
    state( 'false', style( { transform: 'rotate(180deg)' } ) ),
    transition( 'true => false', animate( '400ms ease-out' ) ),
    transition( 'false => true', animate( '400ms ease-in' ) )
] )


@Component( {
    selector: 'app-participant',
    templateUrl: './participant.component.html',
    styleUrls: [ './participant.component.scss' ],
    animations: [
        fadeAnimation, listAnimation, rotatedState
    ],
    providers: [ ManageOlympiadsStore ]
} )
export class ParticipantComponent implements OnInit
{
    showOlympiadsList: boolean
    contests$: Observable<Contest[]>

    constructor( private store: ManageOlympiadsStore )
    {
        this.showOlympiadsList = false
        this.contests$ = this.store.contests
    }

    ngOnInit(): void
    {
        this.store.reload()
    }

    calculateHeight(): number
    {
        return footerHeight
    }

    collapseOlympiadsList(): void
    {
        this.showOlympiadsList = !this.showOlympiadsList
    }
}