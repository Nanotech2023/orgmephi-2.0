import { Component, OnDestroy, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import { Contest, TaskForUserResponseTaskParticipant, Variant } from '@api/tasks/model'
import { ContestAssignmentStore } from '@/contests/containers/contest-assignment/contest-assignment.store'
import { ActivatedRoute } from '@angular/router'


@Component( {
    selector: 'app-contest-assignment',
    templateUrl: './contest-assignment.component.html',
    styleUrls: [ './contest-assignment.component.scss' ],
    providers: [ ContestAssignmentStore ]
} )
export class ContestAssignmentComponent implements OnInit, OnDestroy
{
    contestId!: number | null
    // interval!: number
    viewModel$: Observable<{ loading: boolean; error: string | null; contest: Contest | undefined; variant: Variant | undefined; tasks: Array<TaskForUserResponseTaskParticipant>; time: number | undefined }>

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
            }
        } )
        this.viewModel$ = this.contestAssignmentStore.viewModel$
    }

    getDisplayTime( timeLeft: number | undefined ): string
    {
        if ( timeLeft === undefined )
            return ""
        return new Date( timeLeft * 1000 ).toISOString().substr( 11, 8 )
    }

    ngOnInit(): void
    {
        // this.interval = setInterval( () =>
        // {
        //     if ( this.timeLeft > 0 )
        //     {
        //         this.timeLeft--
        //     }
        //     else
        //     {
        //         this.timeLeft = 60
        //     }
        // }, 1000 )
    }

    ngOnDestroy(): void
    {
        // clearInterval( this.interval )
    }
}
