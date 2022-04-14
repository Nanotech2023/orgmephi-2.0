import { Component, Input } from '@angular/core'


@Component( {
    selector: 'app-contest-details-register',
    templateUrl: './contest-details-register.component.html',
    styleUrls: [ './contest-details-register.component.scss' ]
} )
export class ContestDetailsRegisterComponent
{
    @Input() proctorLogin!: string
    @Input() proctorPassword!: string
}