import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import {
    SimpleContest,
    UserExternalDataResponseTaskParticipant,
    UserProctoringDataResponseTaskParticipant
} from '@api/tasks/model'
import { ActivatedRoute } from '@angular/router'
import { getClassesForDisplay, getStatusDisplay, getSubjectDisplay } from '@/shared/localizeUtils'
import { ContestDetailsStore } from '@/contests/containers/contest-details/contest-details.store'
import { UserResultsForContestResponse } from '@api/responses/model'


@Component( {
    selector: 'app-contest-details',
    templateUrl: './contest-details.component.html',
    styleUrls: [ './contest-details.component.scss' ],
    providers: [ ContestDetailsStore ]
} )
export class ContestDetailsComponent
{
    contest$: Observable<SimpleContest | undefined>
    contestId!: number | null
    isFilledProfile$: Observable<boolean>
    contestResult$: Observable<UserResultsForContestResponse | undefined>
    contestProctoringData$: Observable<UserProctoringDataResponseTaskParticipant | undefined>
    contestFinalStageData$: Observable<UserExternalDataResponseTaskParticipant | undefined>

    constructor( private contestDetailsStore: ContestDetailsStore, private route: ActivatedRoute )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.contestId = Number( paramMap.get( 'contestId' ) )
            if ( !!this.contestId )
            {
                this.contestDetailsStore.fetchUnfilledProfile()
                this.contestDetailsStore.fetchSingle( this.contestId )
                this.contestDetailsStore.fetchProctoringData( this.contestId )
                this.contestDetailsStore.fetchFinalStageData( this.contestId )
                this.contestDetailsStore.fetchAllResults()
            }
        } )
        this.contest$ = this.contestDetailsStore.contest$
        this.contestResult$ = this.contestDetailsStore.contestResult$
        this.contestProctoringData$ = this.contestDetailsStore.contestProctoringData$
        this.contestFinalStageData$ = this.contestDetailsStore.contestFinalStageData$
        this.isFilledProfile$ = this.contestDetailsStore.isFilledProfile$
    }

    getTargetClassesDisplay( contest: SimpleContest ): string
    {
        return getClassesForDisplay( contest )
    }

    getStatusForDisplay( contest: SimpleContest ): string
    {
        return getStatusDisplay( contest )
    }

    getSubjectDisplay( contest: SimpleContest ): string
    {
        return getSubjectDisplay( contest.base_contest?.subject )
    }

    getProfileText( isFilledProfile: boolean | null ): string
    {
        return isFilledProfile ? "Анкета заполнена" : "Заполнить анкету"
    }
}