import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { ContestsStore } from '@/contests/contests.store'
import { SimpleContest } from '@api/tasks/model'
import { ActivatedRoute } from '@angular/router'
import { getClassesForDisplay, getStatusDisplay, getSubjectDisplay } from '@/shared/displayUtils'


@Component( {
    selector: 'app-contest-details',
    templateUrl: './contest-details.component.html',
    styleUrls: [ './contest-details.component.scss' ]
} )
export class ContestDetailsComponent
{
    contest$: Observable<SimpleContest | undefined>
    contestId!: number | null
    isFilledProfile$: Observable<boolean>

    constructor( private route: ActivatedRoute, private contestsStore: ContestsStore )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.contestId = Number( paramMap.get( 'contestId' ) )
            if ( !!this.contestId )
            {
                this.contestsStore.fetchUnfilledProfile()
                this.contestsStore.fetchSingle( this.contestId )
            }
        } )
        this.contest$ = this.contestsStore.contest$
        this.isFilledProfile$ = this.contestsStore.isFilledProfile$
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