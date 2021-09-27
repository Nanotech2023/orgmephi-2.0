import { Component, OnDestroy, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import { SimpleContestWithFlagResponseTaskParticipant } from '@api/tasks/model'
import { ContestsStore } from '@/contests/contests.store'


@Component( {
    selector: 'app-contest-assignment',
    templateUrl: './contest-assignment.component.html',
    styleUrls: [ './contest-assignment.component.scss' ]
} )
export class ContestAssignmentComponent implements OnInit, OnDestroy
{
    contest$: Observable<SimpleContestWithFlagResponseTaskParticipant | undefined>
    timeLeft: number = 14400
    interval!: number

    constructor( private contestsStore: ContestsStore )
    {
        this.contest$ = this.contestsStore.selectedContest
    }

    getDisplayTime(): string
    {
        return new Date( this.timeLeft * 1000 ).toISOString().substr( 11, 8 )
    }

    ngOnInit(): void
    {
        this.interval = setInterval( () =>
        {
            if ( this.timeLeft > 0 )
            {
                this.timeLeft--
            }
            else
            {
                this.timeLeft = 60
            }
        }, 1000 )
    }

    ngOnDestroy(): void
    {
        clearInterval( this.interval )
    }
}
