import { Component } from '@angular/core'
import { footerHeight } from '@/shared/consts'
import { Observable } from 'rxjs'
import { ContestsInStage } from '@/olympiads/tasks/model/contestsInStage'
import { TasksServiceMock } from '@/olympiads/tasks/api/tasks.service.mock'
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
    selector: 'app-participant',
    templateUrl: './participant.component.html',
    styleUrls: [ './participant.component.scss' ],
    animations: [
        fadeAnimation, listAnimation, rotatedState
    ]
} )


export class ParticipantComponent
{
    showOlympiadsList: boolean
    olympiads$: Observable<ContestsInStage>


    constructor( private service: TasksServiceMock )
    {
        this.showOlympiadsList = false
        this.olympiads$ = this.service.olympiadAllGet()
    }

    calculateHeight(): number
    {
        return footerHeight
    }

    collapseOlympiadsList( event: Event ): void
    {
        this.showOlympiadsList = !this.showOlympiadsList
    }
}