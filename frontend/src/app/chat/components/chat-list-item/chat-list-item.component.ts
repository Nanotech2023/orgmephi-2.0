import { Component, Input, OnInit } from '@angular/core'

@Component({
  selector: 'app-chat-list-item',
  templateUrl: './chat-list-item.component.html',
  styleUrls: ['./chat-list-item.component.scss']
})
export class ChatListItemComponent implements OnInit {

  @Input() responder!: string
  @Input() lastMessage!: string
  constructor() { }

  ngOnInit(): void {
  }

}
