import { Component, OnDestroy, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import {
    Contest,
    TaskForUserResponseTaskParticipant,
    VariantWithCompletedTasksCountTaskParticipant
} from '@api/tasks/model'
import { ContestAssignmentStore } from '@/contests/containers/contest-assignment/contest-assignment.store'
import { ActivatedRoute } from '@angular/router'
import { UserResponseStatusResponse } from '@api/responses/model'


@Component( {
    selector: 'app-contest-assignment',
    templateUrl: './contest-assignment.component.html',
    styleUrls: [ './contest-assignment.component.scss' ],
    providers: [ ContestAssignmentStore ]
} )
export class ContestAssignmentComponent implements OnInit, OnDestroy
{
    contestId!: number | null
    // @ts-ignore
    interval!
    viewModel$: Observable<{ loading: boolean; error: string | null; contest: Contest | undefined; variant: VariantWithCompletedTasksCountTaskParticipant | undefined; tasks: Array<TaskForUserResponseTaskParticipant>; time: number | undefined; status: UserResponseStatusResponse.StatusEnum | undefined }>
    timeLeft: number | undefined

    constructor( private route: ActivatedRoute, private contestAssignmentStore: ContestAssignmentStore )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.contestId = Number( paramMap.get( 'contestId' ) )
            if ( !!this.contestId )
            {
                this.contestAssignmentStore.fetchContest( this.contestId )
                this.contestAssignmentStore.fetchVariant( this.contestId )
                this.contestAssignmentStore.fetchTasks( this.contestId )
                this.contestAssignmentStore.fetchTime( this.contestId )
                this.contestAssignmentStore.fetchStatus( this.contestId )
            }
        } )
        this.viewModel$ = this.contestAssignmentStore.viewModel$
    }

    getDisplayTime( time: number | undefined ): string
    {
        if ( this.timeLeft === undefined )
        {
            this.timeLeft = time
            return ""
        }
        return new Date( this.timeLeft * 1000 ).toISOString().substr( 11, 8 )
    }

    ngOnInit(): void
    {
        this.interval = setInterval( () =>
        {
            if ( this.timeLeft === undefined )
                return
            if ( this.timeLeft > 0 )
            {
                this.timeLeft--
            }
            else
            {
                this.timeLeft = 0
            }
        }, 1000 )
    }

    ngOnDestroy(): void
    {
        clearInterval( this.interval )
    }

    finish(): void
    {
        if ( this.contestId !== null )
        {
            this.contestAssignmentStore.finish( this.contestId )
            this.contestAssignmentStore.fetchTime( this.contestId )
        }
    }
}