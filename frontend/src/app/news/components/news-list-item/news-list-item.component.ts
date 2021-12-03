import { Component, Input, OnInit } from '@angular/core'


@Component( {
    selector: 'app-news-list-item',
    templateUrl: './news-list-item.component.html',
    styleUrls: [ './news-list-item.component.scss' ]
} )
export class NewsListItemComponent implements OnInit
{
    @Input() newsTitle! : string
    @Input() newsText!: string
    @Input() newsType!: string
    @Input() newsDate!: string
    @Input() newsImage!: string

    constructor() { }

    ngOnInit(): void
    {
    }

}
