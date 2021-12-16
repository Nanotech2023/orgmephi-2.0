import { Component } from '@angular/core'
import { ContestAssignmentStore } from '@/contests/containers/contest-assignment/contest-assignment.store'
import { Observable } from 'rxjs'
import {
    Contest,
    TaskForUserResponseTaskParticipant,
    VariantWithCompletedTasksCountTaskParticipant
} from '@api/tasks/model'
import { UserResponseStatusResponse } from '@api/responses/model'
import { ActivatedRoute } from '@angular/router'


@Component( {
    selector: 'app-contest-assignment-results',
    templateUrl: './contest-assignment-results.component.html',
    styleUrls: [ './contest-assignment-results.component.scss' ],
    providers: [ ContestAssignmentStore ]
} )
export class ContestAssignmentResultsComponent
{
    contestId!: number | null
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
                this.contestAssignmentStore.fetchStatus( this.contestId )
            }
        } )
        this.viewModel$ = this.contestAssignmentStore.viewModel$
    }
}
