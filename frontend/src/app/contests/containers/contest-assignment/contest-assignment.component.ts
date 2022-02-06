import { Component, OnDestroy, OnInit } from '@angular/core'
import { interval, Observable, Subscription } from 'rxjs'
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
    viewModel$: Observable<{ loading: boolean; error: string | null; contest: Contest | undefined; variant: VariantWithCompletedTasksCountTaskParticipant | undefined; tasks: Array<TaskForUserResponseTaskParticipant>; time: string; status: UserResponseStatusResponse.StatusEnum | undefined }>
    timeLeft: number | undefined
    reloadTimerSubscription!: Subscription

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

    ngOnInit(): void
    {
        this.reloadTimerSubscription = interval( 1000 ).subscribe( _ =>
        {
            if ( !!this.contestId )
                this.contestAssignmentStore.fetchTime( this.contestId )
        } )
    }

    ngOnDestroy(): void
    {
        this.reloadTimerSubscription.unsubscribe()
    }

    finish(): void
    {
        if ( !!this.contestId )
        {
            this.contestAssignmentStore.finish( this.contestId )
            this.contestAssignmentStore.fetchTime( this.contestId )
        }
    }
}