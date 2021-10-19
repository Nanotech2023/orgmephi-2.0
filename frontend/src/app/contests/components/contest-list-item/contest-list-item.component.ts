import { Component, Input } from '@angular/core'
import { SimpleContest, SimpleContestWithFlagResponseTaskParticipant, TargetClass } from '@api/tasks/model'
import { Router } from '@angular/router'
import { ContestsStore } from '@/contests/contests.store'


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
        let targetClasses = this.contest.contest?.base_contest?.target_classes as TargetClass[]
        if ( targetClasses && targetClasses.length )
        {
            return `${ targetClasses[ 0 ].target_class }-${ targetClasses[ targetClasses.length - 1 ].target_class }`
        }
        return ""
    }

    getStatusDisplay(): string
    {
        switch ( this.contest.contest?.status )
        {
            case SimpleContest.StatusEnum.WillStartSoon:
                return "Скоро начнётся"
            case SimpleContest.StatusEnum.InProgress:
                return "Проходит"
            case SimpleContest.StatusEnum.Finished:
                return "Олимпиада завершена"
            default:
                return "Скоро начнётся"
        }
    }
}
