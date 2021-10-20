import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { SchoolInfo } from '@api/users/models'


@Component( {
    selector: 'app-yes-no-component',
    templateUrl: './yes-no-component.component.html',
    styleUrls: [ './yes-no-component.component.scss' ]
} )
export class YesNoComponentComponent
{
    @Input() model!: boolean
    @Input() radioId!: string
    @Output() modelChange = new EventEmitter<boolean>()

    checked( b: boolean )
    {
        return this.model === b
    }

    nameYes()
    {
        return `${ this.radioId }Yes`
    }

    nameNo()
    {
        return `${ this.radioId }No`
    }

    onChecked( b: boolean )
    {
        this.modelChange.emit( b )
    }
}
