import { Component, Input } from '@angular/core'
import { SimpleContestWithFlagResponseTaskParticipant } from '@api/tasks/model'
import { Router } from '@angular/router'
import { getClassesForDisplay, getStatusDisplay, getSubjectDisplay } from '@/shared/displayUtils'


@Component( {
    selector: 'app-contest-list-item',
    templateUrl: './contest-list-item.component.html',
    styleUrls: [ './contest-list-item.component.scss' ]
} )
export class ContestListItemComponent
{
    @Input() contest!: SimpleContestWithFlagResponseTaskParticipant

    constructor( private router: Router )
    {
    }

    navigateTo(): Promise<boolean>
    {
        return this.router.navigate( [ "/contests", this.contest.contest?.contest_id ] )
    }

    getClassesForDisplay(): string
    {
        return getClassesForDisplay( this.contest.contest )
    }

    getStatusDisplay(): string
    {
        return getStatusDisplay( this.contest.contest )
    }

    getSubjectDisplay()
    {
        return getSubjectDisplay( this.contest.contest?.base_contest?.subject )
    }
}
