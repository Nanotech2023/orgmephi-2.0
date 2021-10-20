import { Component, Input } from '@angular/core'
import { SimpleContestWithFlagResponseTaskParticipant, TargetClass } from '@api/tasks/model'
import { Router } from '@angular/router'
import { ContestsStore } from '@/contests/contests.store'
import { getClassesForDisplay, getStatusDisplay } from '@/shared/displayUtils'


@Component( {
    selector: 'app-contest-list-item',
    templateUrl: './contest-list-item.component.html',
    styleUrls: [ './contest-list-item.component.scss' ]
} )
export class ContestListItemComponent
{
    @Input() contest!: SimpleContestWithFlagResponseTaskParticipant

    constructor( private contestsStore: ContestsStore, private router: Router )
    {
    }

    navigateTo(): Promise<boolean>
    {
        // TODO allow select other locations
        const locationId = 3
        if ( this.contest.contest )
        {
            this.contestsStore.enroll( {
                contestId: this.contest.contest.contest_id as number,
                locationId: locationId
            } )
            this.contestsStore.selectContest( this.contest.contest )
        }
        return this.router.navigate( [ "/contests", this.contest.contest?.contest_id ] )
    }

    getClassesForDisplay(): string
    {
        return getClassesForDisplay(this.contest.contest)
    }

    getStatusDisplay(): string
    {
        return getStatusDisplay( this.contest.contest )
    }
}
