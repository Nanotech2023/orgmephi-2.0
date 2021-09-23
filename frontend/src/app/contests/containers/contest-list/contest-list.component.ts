import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { Contest } from '@api/tasks/model'
import { ContestsStore } from '@/contests/contests.store'
import { footerHeight } from '@/shared/consts'
import { animate, query, stagger, state, style, transition, trigger } from '@angular/animations'


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
    selector: 'app-contest-list',
    templateUrl: './contest-list.component.html',
    styleUrls: [ './contest-list.component.scss' ],
    animations: [
        fadeAnimation, listAnimation, rotatedState
    ]
} )
export class ContestListComponent implements OnInit
{
    isParticipant$!: Observable<boolean>

    showContestsList: boolean
    contests$: Observable<Contest[]>

    constructor( private authStore: Store<AuthState.State>, private contestsStore: ContestsStore )
    {
        this.showContestsList = false
        this.contests$ = this.contestsStore.contests
    }

    ngOnInit(): void
    {
        this.isParticipant$ = this.authStore.pipe( select( AuthSelectors.selectIsParticipant ) )
        this.contestsStore.fetchAll()
    }

    calculateHeight(): number
    {
        return footerHeight
    }

    collapseContestsList(): void
    {
        this.showContestsList = !this.showContestsList
    }
}
