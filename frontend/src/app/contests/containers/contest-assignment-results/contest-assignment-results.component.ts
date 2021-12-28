import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { Contest } from '@api/tasks/model'
import { BaseAnswer, TaskForUserResponseResults, UserResultForContestResponse } from '@api/responses/model'
import { ActivatedRoute } from '@angular/router'
import {
    ContestAssignmentResultsStore
} from '@/contests/containers/contest-assignment-results/contest-assignment-results.store'


@Component( {
    selector: 'app-contest-assignment-results',
    templateUrl: './contest-assignment-results.component.html',
    styleUrls: [ './contest-assignment-results.component.scss' ],
    providers: [ ContestAssignmentResultsStore ]
} )
export class ContestAssignmentResultsComponent
{
    contestId!: number | null
    viewModel$: Observable<{ loading: boolean; error: string | null; contest: Contest | undefined; results: UserResultForContestResponse | undefined }>
    timeLeft: number | undefined
    answer!: UserResultForContestResponse

    constructor( private route: ActivatedRoute, private store: ContestAssignmentResultsStore )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.contestId = Number( paramMap.get( 'contestId' ) )
            if ( !!this.contestId )
            {
                this.store.fetchContest( this.contestId )
                this.store.fetchResults( this.contestId )
            }
        } )

        this.viewModel$ = this.store.viewModel$
    }

    getUserAnswerForTask( answers: Array<BaseAnswer> | undefined, task: TaskForUserResponseResults ): BaseAnswer | undefined
    {
        return answers !== undefined ? answers.find( item => item.task_id == task.task_id ) : undefined
    }

    getUserMark( viewModel: Array<BaseAnswer> | undefined ): number
    {
        return viewModel == null ? 0 : viewModel.reduce( ( result, item ) => result + ( item.mark ?? 0 ), 0 )
    }

    getMaxMark( tasks_list: Array<TaskForUserResponseResults> | undefined ): number
    {
        return tasks_list == null ? 0 : tasks_list.reduce( ( result, item ) => result + ( item.task_points ?? 0 ), 0 )
    }
}
