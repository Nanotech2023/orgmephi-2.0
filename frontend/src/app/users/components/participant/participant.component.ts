import { Component } from '@angular/core'


@Component( {
    selector: 'app-participant',
    templateUrl: './participant.component.html',
    styleUrls: [ './participant.component.scss' ]
} )
export class ParticipantComponent
{
    calculateHeight(): number
    {
        return window.innerHeight - ( 125 + 167 )
    }
}